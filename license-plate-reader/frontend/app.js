// Image preview
document.getElementById("imageInput").addEventListener("change", function(e) {
    const file = e.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const originalImage = document.getElementById("originalImage");
            originalImage.src = e.target.result;
            originalImage.style.display = "block";
        };
        reader.readAsDataURL(file);
    }
});

document.getElementById("uploadForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    const formData = new FormData();
    const fileInput = document.getElementById("imageInput");
    formData.append("image", fileInput.files[0]);

    const resultDiv = document.getElementById("result");
    resultDiv.innerHTML = '<p class="processing">Processing...</p>';

    try {
        const response = await fetch("http://127.0.0.1:5000/upload", {
            method: "POST",
            body: formData,
        });

        const result = await response.json();
        console.log(result);
        
        // Update detected image
        if (result.detection_image) {
            const detectedImage = document.getElementById("detectedImage");
            detectedImage.src = `data:image/jpeg;base64,${result.detection_image}`;
            detectedImage.style.display = "block";
        }

        if (result.error) {
            resultDiv.innerHTML = `<p class="error">Error: ${result.error}</p>`;
        } else if (result.plates.length > 0) {
            resultDiv.innerHTML = `
                <p class="success">
                    Detected License Plates:<br>
                    ${result.plates.map(plate => `<span class="plate-text">${plate}</span>`).join("<br>")}
                </p>`;
        } else {
            resultDiv.innerHTML = '<p class="error">No license plates detected.</p>';
        }
    } catch (error) {
        resultDiv.innerHTML = `<p class="error">Error: ${error.message}</p>`;
    }
});