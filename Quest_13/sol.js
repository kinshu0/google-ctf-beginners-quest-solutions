function decryptWithMilitaryGradeEncryption(hexstr) {
    const len = hexstr.length;
  
    const key = Uint8Array.from([
      11, 22, 33, 44, 55, 66, 77, 88, 99, 101, 202
    ]);
    const keylen = key.length;
  
    const arr = [];
  
    for (let i = 0; i < len; i += 2) {
      const byte = parseInt(hexstr.substring(i, i + 2), 16);
      arr.push(byte ^ key[(i >> 1) % keylen]);
    }
  
    const decoder = new TextDecoder();
    return decoder.decode(Uint8Array.from(arr));
  }

const messages = [
    { "militaryGradeEncryption": true, "codename": "BadGuy87", "message": "717f510b44623d391016bd6464450c5e316d1a0c16b95f794d487a2719373000be4a54445843273f080216b97c795348642d19300a169d627a4d645634280c0c21a53a241218" },
    { "militaryGradeEncryption": true, "codename": "Goon8133", "message": "67794d0c452e3467" },
    { "militaryGradeEncryption": true, "codename": "BadGuy87", "message": "72734044" }
]


const messagesDecrypted = messages.map(mes => decryptWithMilitaryGradeEncryption(mes.message))

console.log(messagesDecrypted)