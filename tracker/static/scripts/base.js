const errorContainer = $(".error-container");
const contentContainer = $(".content-container");


$(".nav-button").click(event => {
    const route = $(event.currentTarget).attr("id").split("-")[0]
    window.location.replace(`/${route}`);
    $(".active-border").addClass("invisible")
    $(event.currentTarget).prev().removeClass("invisible")
    console.log($(event.currentTarget).prev())
})

$(".line-container").each((index, element) => {
    const percent = $(element).attr("data-percent");
    $(element).children(".yellow-scale-line").css("width", percent+"%");
})

function emptyErrorContainer() {
    errorContainer.empty();
}


function fetchTerms() {
    return fetch("/get_terms", {
        method: "GET",
        headers: {
            "Content-Type": "application/json"
        }
    })
        .then(response => response.json())
        .then(response => {
            return response.terms;
        })
        .catch(error => {
            console.log('Unhappy little error :(', error);
        });
}

function fetchSubjectsForTerm(term) {
    return fetch(`/get_subjects?term=${term}`, {
        method: "GET",
        headers: {
            "Content-Type": "application/json"
        }
    })
        .then(response => response.json())
        .then(response => {
            console.log(response.subjects);
            return response.subjects;
        })
        .catch(error => {
            console.log('Unhappy little error :(', error);
        });
}



