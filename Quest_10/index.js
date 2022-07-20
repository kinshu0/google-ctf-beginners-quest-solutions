window.onload = main



async function readCSV(url) {
    const res = await fetch(url)
    const text = await res.text()

    return text.split('\n')
        .map(line => line.split(',').map(col => parseFloat(col)))
    
}


function main() {

    const canvas = document.getElementById('vga-display')
    const ctx = canvas.getContext('2d')

    const img = ctx.createImageData(canvas.width, canvas.height)

    const { data } = img

    for (let i = 0; i < data.length; i += 4) {
        data[i] = 255
        data[i + 3] = 255
    }


    ctx.putImageData(img, 0, 0);


    console.log(canvas.width, canvas.height)


    // console.image(leak)

    // ctx.fillstyle = 'rgb(200,0,0)'
    // ctx.fillRect(10, 10, 50, 50)


    readCSV('1.csv').then(res => console.log(res.slice(10)))

}
