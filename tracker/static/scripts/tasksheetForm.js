const form = $("form");
const subjectName = form.attr("data-subject-name");
const tasksheetNumber = form.attr("data-tasksheet-number");

$("#submit-new-tasksheet-btn").click(event => {
    emptyErrorContainer();
    postFormData("/points/add_new_tasksheet");
})


$("#edit-tasksheet-btn").click(event => {
    emptyErrorContainer();
    postFormData(window.location);
})


$("#cancel-new-tasksheet-btn").click(() => {
    window.location.replace(`/points/${subjectName}`);
})


$("#remove-tasksheet-btn").click(() => {
    fetchRemoveRequest();
})


function fetchRemoveRequest() {
    fetch(`/remove/${subjectName}/${tasksheetNumber}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        }
    })
        .then(response => response.json())
        .then(response => {
            if (response.success === true) {
                window.location.replace(`/points/${subjectName}`);
            } else {
                console.log("ERROR");
                console.log(response);
                $(".error-container").append(`<p>${response.message}</p>`);
            }
        })
        .catch(error => {
            console.log('Unhappy little error :(', error);
        });
}


function postFormData(path){
    console.log(subjectName)
    fetch(path, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            subjectName: subjectName,
            number: $("#tasksheet-number").val(),
            points: $("#points_received").val(),
            maxPoints: $("#points_max").val(),
        })
    })
        .then(response => response.json())
        .then(response => {
            if (response.success === true) {
                window.location.replace(`/points/${subjectName}`);
            } else {
                console.log("ERROR");
                console.log(response);
                $(".error-container").append(`<p>${response.message}</p>`);
            }
        })
        .catch(error => {
            console.log('Unhappy little error :(', error);
        });
}