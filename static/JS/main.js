document.addEventListener("DOMContentLoaded", () => {
    const button = document.querySelector(".convertir");
    const buttonupdate = document.querySelector(".botonupdate");
    
    button.addEventListener("click", () => {
        button.classList.add("inactive");
        buttonupdate.classList.add("inactive")
        const elementoConvertido = document.body;
        html2pdf()
            .set({
                margin: .5,
                filename: 'documento.pdf',
                image: {
                    type: 'jpeg',
                    quality: 0.98
                },
                html2canvas: {
                    scale: 3, // A mayor escala, mejores gráficos, pero más peso
                    letterRendering: true,
                },
                jsPDF: {
                    unit: "in",
                    format: "a4",
                    orientation: 'portrait' // landscape o portrait
                }
            })
            .from(elementoConvertido)
            .save()
            .catch(err => console.log(err))
            .finally()
            .then(() => {
                console.log("guardado")
                button.classList.remove("inactive");
                buttonupdate.classList.remove("inactive");
                const myform = document.querySelector(".myform").reset();
            })
    })
});