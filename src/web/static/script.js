let image = document.querySelector("#image");

async function update(){
    let r = await fetch("/image");
    let blob = await r.blob()

    let url = URL.createObjectURL(blob);
    image.src = url;
}

setInterval(update, 1000);