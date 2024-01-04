liff.ready.then(() => {
    // Get current date and time
    const currentDate = new Date().toISOString().slice(0, 16);
    console.log(currentDate);

    // Set the default value for the startDateTimePicker input field
    document.getElementById('startDateTimePicker').value = currentDate;

    // Set the default value for the endDateTimePicker input field
    document.getElementById('endDateTimePicker').value = currentDate;


    document.getElementById("leaveForm").addEventListener("submit", function (event) {
        event.preventDefault(); // Prevent the default form submission

        // Get form data
        const formData = new FormData(event.target);
        const formDataObject = {};
        formData.forEach((value, key) => {
            formDataObject[key] = value;
        });

        // Send POST request
        fetch("/liff/app/call-off", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(formDataObject),
        }).then(
            response => response.json()
        ).then(data => {
            console.log("Success:", data);
            // Handle success response
            window.location.href = clientHost + "/liff/summary";

        }).catch(error => {
            console.error("Error:", error);
            // Handle error
        });
    });
});

