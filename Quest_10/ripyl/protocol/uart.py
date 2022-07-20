#!/usr/bin/python
# -*- coding: utf-8 -*-

'''UART protocol decoder
'''

# Copyright © 2013 Kevin Thibedeau

# This file is part of Ripyl.

# Ripyl is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation, either version 3 of
# the License, or (at your option) any later version.

# Ripyl is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public
# License along with Ripyl. If not, see <http://www.gnu.org/licenses/>.

from __future__ import print_function, division

import itertools

from ripyl.decode import *
import ripyl.streaming as stream
from ripyl.util.enum import Enum


class AutoBaudError(stream.StreamError):
    '''Error for failed baud rate detection'''
    pass


class UARTStreamStatus(Enum):
    '''Enumeration of UART status codes'''
    FramingError = stream.StreamStatus.Error + 1
    ParityError = stream.StreamStatus.Error + 2

class UARTFrame(stream.StreamSegment):
    '''Frame object for UART data'''
    def __init__(self, bounds, data=None, status=stream.StreamStatus.Ok):
        stream.StreamSegment.__init__(self, bounds, data, status=status)
        self.kind = 'UART frame'

    @classmethod
    def status_text(cls, status):
        if status >= UARTStreamStatus.FramingError and \
            status <= UARTStreamStatus.ParityError:
            
            return UARTStreamStatus(status)
        else:
            return stream.StreamSegment.status_text(status)

    def __str__(self):
        return chr(self.data & 0xFF)
        

class UARTConfig(Enum):
    '''Enumeration of configuration settings'''
    IdleHigh = 1  # Polarity settings
    IdleLow = 2

def uart_decode(stream_data, bits=8, parity=None, stop_bits=1.0, lsb_first=True, polarity=UARTConfig.IdleHigh, \
    baud_rate=None, use_std_baud=True, logic_levels=None, stream_type=stream.StreamType.Samples, param_info=None):
    
    '''Decode a UART data stream

    This is a generator function that can be used in a pipeline of waveform
    procesing operations.

    Sample streams are a sequence of SampleChunk Objects. Edge streams are a sequence
    of 2-tuples of (time, int) pairs. The type of stream is identified by the stream_type
    parameter. Sample streams will be analyzed to find edge transitions representing
    0 and 1 logic states of the waveforms. With sample streams, an initial block of data
    is consumed to determine the most likely logic levels in the signal.

    stream_data (iterable of SampleChunk objects or (float, int) pairs)
        A sample stream or edge stream representing a serial data signal.

    bits (int)
        The number of bits in each word. Typically 5, 7, 8, or 9.
    
    parity (string or None)
        The type of parity to use. One of None, 'even', or 'odd'
    
    stop_bits (number)
        The number of stop bits. Typically 1, 1.5, or 2
    
    lsb_first (bool)
        Flag indicating whether the Least Significant Bit is transmitted first.
    
    inverted (bool)
        Flag indicating if the signal levels have been inverted from their logical
        meaning. Use this when the input stream derives from an inverting driver such
        as those used for RS-232.
    polarity (UARTConfig)
        Set the polarity (idle state high or low).
    
    baud_rate (int)
        The baud rate of the stream. If None, the first 50 edges will be analyzed to
        automatically determine the most likely baud rate for the stream. On average
        50 edges will occur after 11 frames have been captured.
    
    use_std_baud (bool)
        Flag that forces coercion of automatically detected baud rate to the set of
        standard rates
        
    logic_levels ((float, float) or None)
        Optional pair that indicates (low, high) logic levels of the sample
        stream. When present, auto level detection is disabled. This has no effect on
        edge streams.
    
    stream_type (streaming.StreamType)
        A StreamType value indicating that the stream parameter represents either Samples
        or Edges
        
    param_info (dict or None)
        An optional dictionary object that is used to monitor the results of
        automatic baud detection.

        
    Yields a series of UARTFrame objects. Each frame contains subrecords marking the location
      of sub-elements within the frame (start, data, parity, stop). Parity errors are recorded
      as an error status in the parity subrecord. BRK conditions are reported as a data value
      0x00 with a framing error in the status code.
      
    Raises AutoLevelError if stream_type = Samples and the logic levels cannot
      be determined.
      
    Raises AutoBaudError if auto-baud is active and the baud rate cannot
      be determined.
      
    Raises ValueError if the parity argument is invalid.
    '''

    bits = int(bits)
    
    if stream_type == stream.StreamType.Samples:
        if logic_levels is None:
            samp_it, logic_levels = check_logic_levels(stream_data)
        else:
            samp_it = stream_data
        
        edges = find_edges(samp_it, logic_levels, hysteresis=0.4)
    else: # the stream is already a list of edges
        edges = stream_data
        
    
    raw_symbol_rate = 0
    
    if baud_rate is None:
        # Find the baud rate
        
        # tee off an independent iterator to determine baud rate
        edges_it, sre_it = itertools.tee(edges)
        
        # Experiments on random data indicate that find_symbol_rate() will almost
        # always converge to a close estimate of baud rate within the first 35 edges.
        # It seems to be a guarantee after 50 edges (pathological cases not withstanding).
        min_edges = 50
        symbol_rate_edges = itertools.islice(sre_it, min_edges)
        
        # We need to ensure that we can pull out enough edges from the iterator slice
        # Just consume them all for a count        
        sre_list = list(symbol_rate_edges)
        if len(sre_list) < min_edges:
            raise AutoBaudError('Unable to compute automatic baud rate. Insufficient edges.')
        
        raw_symbol_rate = find_symbol_rate(iter(sre_list), spectra=2)

        if raw_symbol_rate == 0:
            # Some special data sequences may lack a second harmonic which
            # ruins the HPS used in find_symbol_rate().

            # In this case we bypass the HPS and just take the symbol rate using the dominant span
            raw_symbol_rate = find_symbol_rate(iter(sre_list), spectra=1)

        # delete the tee'd iterators so that the internal buffer will not grow
        # as the edges_it is advanced later on
        del symbol_rate_edges
        del sre_it
        
        std_bauds = (110, 300, 600, 1200, 2400, 4800, 9600, 14400, 19200, 28800, 38400, \
                     56000, 57600, 115200, 128000, 153600, 230400, 256000, 460800, 921600)

        if use_std_baud:
            # find the standard baud closest to the raw rate
            baud_rate = min(std_bauds, key=lambda x: abs(x - raw_symbol_rate))
        else:
            baud_rate = raw_symbol_rate
            
        #print('@@@@@@@@@@ baud rate:', baud_rate, raw_symbol_rate)

        if baud_rate == 0:
            raise AutoBaudError('Unable to compute automatic baud rate. Got 0.')

    else:
        edges_it = edges

    # Invert edge polarity if idle-low
    if polarity == UARTConfig.IdleLow:
        edges_it = ((t, 1 - e) for t, e in edges_it)
        
    if param_info is not None:
        param_info['baud_rate'] = baud_rate
        param_info['raw_symbol_rate'] = raw_symbol_rate
        if stream_type == stream.StreamType.Samples:
            param_info['logic_levels'] = logic_levels

    bit_period = 1.0 / float(baud_rate)
    es = EdgeSequence(edges_it, bit_period)
    
    # Now we start the actual decode process
    
    mark = 1
    space = 0
        
    # initialize to point where state is 'mark' --> idle time before first start bit
    while es.cur_state() == space and not es.at_end():
        es.advance_to_edge()
        
    #print('start bit', es.cur_time)
    
    while not es.at_end():
        # look for start bit falling edge
        es.advance_to_edge()
        #print('### advance:', es.cur_time)
        
        # We could have an anamolous edge at the end of the edge list
        # Check if edge sequence is complete after our advance
        if es.at_end():
            break

        # We should be at the start of the start bit (space)
        # If not then the previous character was likely a BRK condition and
        # we just now returned to idle (mark).
        if es.cur_state() != space:
            continue
        
        start_time = es.cur_time
        data_time = es.cur_time + bit_period
        es.advance(bit_period * 1.5) # move to middle of first data bit
        
        byte = 0
        cur_bit = 0
        
        p = 0
        if parity is not None:
            if parity.lower() == 'even':
                p = 0
            elif parity.lower() == 'odd':
                p = 1
            else:
                raise ValueError('Invalid parity argument')
                
        while cur_bit < bits:
            bit_val = es.cur_state()
            
            p ^= bit_val
            if lsb_first:
                byte = byte >> 1 | (bit_val << (bits-1))
            else:
                byte = byte << 1 | bit_val
                
            cur_bit += 1
            es.advance()
            #print(es.cur_time)
            
        data_end_time = es.cur_time - bit_period * 0.5
        parity_error = False
        if parity is not None:
            parity_time = data_end_time
            parity_val = es.cur_state()
            #print('PB:', p, parity_val)
            # check the parity
            if parity_val != p:
                parity_error = True
            es.advance()
        
        # We are currently 1/2 bit past the last data or parity bit
        stop_time = es.cur_time - bit_period * 0.5
        
        # Verify the stop bit(s)
        if stop_bits > 1.0:
            # Move to within 1/2 bit of the end of the stop bits
            es.advance(bit_period * (stop_bits - 1.0))
            
        framing_error = False
        if es.cur_state() != mark: # Not at idle -> break condition
            framing_error = True
        
        end_time = es.cur_time + bit_period * 0.5
        
        # construct frame objects
        status = UARTStreamStatus.FramingError if framing_error else stream.StreamStatus.Ok
        nf = UARTFrame((start_time, end_time), byte, status=status)
        nf.annotate('frame', {}, stream.AnnotationFormat.Hidden)
        
        nf.subrecords.append(stream.StreamSegment((start_time, data_time), kind='start bit'))
        nf.subrecords[-1].annotate('misc', {'_bits':1}, stream.AnnotationFormat.Invisible)
        nf.subrecords.append(stream.StreamSegment((data_time, data_end_time), byte, kind='data bits'))
        nf.subrecords[-1].annotate('data', {'_bits':bits}, stream.AnnotationFormat.General)
        if parity is not None:
            status = UARTStreamStatus.ParityError if parity_error else stream.StreamStatus.Ok
            nf.subrecords.append(stream.StreamSegment((parity_time, stop_time), kind='parity', status=status))
            nf.subrecords[-1].annotate('check', {'_bits':1}, stream.AnnotationFormat.General)
            
        nf.subrecords.append(stream.StreamSegment((stop_time, end_time), kind='stop bit'))
        nf.subrecords[-1].annotate('misc', {'_bits':stop_bits}, stream.AnnotationFormat.Invisible)
            
        yield nf
        #print('### new byte:', es.cur_time, byte, bin(byte), chr(byte))
        
    

def uart_synth(data, bits = 8, baud=115200, parity=None, stop_bits=1.0, idle_start=0.0, idle_end=0.0, \
    word_interval=100.0e-7):
    '''Generate synthesized UART waveform
    
    This function simulates a single, unidirectional channel of a UART serial
    connection. Its output is analagous to txd. The signal is generated with
    idle-high polarity.
    
    This is a generator function that can be used in a pipeline of waveform
    procesing operations.
    
    data (sequence of int)
        A sequence of words that will be transmitted serially
    
    bits (int)
        The number of bits in each word. Typically 5, 7, 8, or 9.
    
    baud (int)
        The baud rate
        
    parity (string or None)
        The type of parity to use. One of None, 'even', or 'odd'
    
    stop_bits (number)
        The number of stop bits. Typically 1, 1.5, or 2
    
    idle_start (float)
        The amount of idle time before the transmission of data begins

    idle_end (float)
        The amount of idle time after the transmission of data ends

    word_interval (float)
        The amount of time between data words

    Yields a series of 2-tuples (time, value) representing the time and
      logic value (0 or 1) for each edge transition on txd. The first tuple
      yielded is the initial state of the waveform. All remaining
      tuples are edges where the txd state changes.
        
    '''
    
    bits = int(bits)
    
    bit_period = 1.0 / baud
    
    t = 0.0
    txd = 1 # idle-high
    
    yield (t, txd) # set initial conditions
    t += idle_start
    
    for d in data:
        txd = 0
        yield (t, txd) # falling edge of start bit
        t += bit_period
        bits_remaining = bits

        p = 0
        if parity is not None:
            if parity.lower() == 'even':
                p = 0
            elif parity.lower() == 'odd':
                p = 1
            else:
                raise ValueError('Invalid parity argument')        
        
        while bits_remaining:
            next_bit = d & 0x01
            p ^= next_bit
            d = d >> 1
            bits_remaining -= 1
            
            if txd != next_bit:
                txd = next_bit
                yield (t, txd)
            t += bit_period
            
        if parity is not None:
            txd = p
            yield (t, txd)
            t += bit_period
            
            
        if txd == 0: 
            txd = 1
            yield (t, txd)
        t += stop_bits * bit_period # add stop bit
        t += word_interval
        
    t += idle_end - word_interval
        
    yield (t, txd)

