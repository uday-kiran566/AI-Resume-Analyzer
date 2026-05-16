document.getElementById("analyze-button").addEventListener("click", function () {

    console.log("Clicked");

    let file = document.getElementById("resumeFile").files[0];
    let jobText = document.getElementById("jobText").value;

    if (!file) {
        alert("Please upload resume file");
        return;
    }

    if (!jobText) {
        alert("Please enter job description");
        return;
    }

    document.getElementById("result").innerText =
        "Analyzing resume...";

    // TEMP demo (replace with Flask API later)
    setTimeout(() => {
        document.getElementById("result").innerText =
            "Job received successfully";
    }, 1500);
});