document.getElementById("uploadForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    const formData = new FormData();
    const fileInput = document.getElementById("imageInput");
    formData.append("image", fileInput.files[0]);

    const resultDiv = document.getElementById("result");
    resultDiv.innerHTML = "Processing...";

    try {
        const response = await fetch("http://127.0.0.1:5000/upload", {
            method: "POST",
            body: formData,
        });

        const result = await response.json();
        console.log(result);
        if (result.error) {
            resultDiv.innerHTML = `Error: ${result.error}`;
        } else if (result.plates.length > 0) {
            resultDiv.innerHTML = `Detected License Plates: <br>${result.plates.join("<br>")}`;
        } else {
            resultDiv.innerHTML = "No license plates detected.";
        }
    } catch (error) {
        resultDiv.innerHTML = `Error: ${error.message}`;
    }
});