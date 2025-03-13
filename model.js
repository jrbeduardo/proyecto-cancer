document.addEventListener("DOMContentLoaded", function() {
    let base64Image = "";

    // Previsualizar la imagen seleccionada
    document.getElementById("image-input").addEventListener("change", function() {
        const file = this.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                document.getElementById("image-preview").src = e.target.result;
                document.getElementById("image-preview").style.display = "block";
                document.getElementById("predict-btn").style.display = "inline-block";
                base64Image = e.target.result.split(',')[1]; // Eliminar el prefijo "data:image/jpeg;base64,"
            };
            reader.readAsDataURL(file); // Leer la imagen y convertirla a base64
        }
    });

    // Enviar la imagen para la predicción
    document.getElementById("predict-btn").addEventListener("click", function() {
        // Mostrar el loader
        document.getElementById("loader").style.display = "inline-block";
        document.getElementById("result").style.display = "none";

        fetch("https://fd7e-35-198-239-245.ngrok-free.app/predict/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                img_base64: base64Image
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error("Error en la respuesta de la API");
            }
            return response.json();
        })
        .then(data => {
            // Añadir un retraso de 2 segundos antes de mostrar los resultados
            setTimeout(() => {
                document.getElementById("prediction-result").textContent = `${data.prediccion} (Confianza: ${data.confianza})`;
                document.getElementById("result").style.display = "block";
            }, 2000); // 2000 milisegundos = 2 segundos
        })
        .catch(error => {
            // Añadir retraso de 2 segundos en caso de error
            setTimeout(() => {
                document.getElementById("prediction-result").textContent = `Error al realizar la predicción: ${error.message}`;
                document.getElementById("result").style.display = "block";
            }, 2000);
        })
        .finally(() => {
            // Ocultar el loader después del retraso
            setTimeout(() => {
                document.getElementById("loader").style.display = "none";
            }, 2000);
        });
    });
});
