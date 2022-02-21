const termInput = $("#term-input");
const termsSelector = $(".terms-selector");

$("#submit-new-subject-btn").click(event => {
    event.preventDefault();
    emptyErrorContainer();
    postFormData("/subjects/add_new_subject");
})

$("#edit-subject-btn").click(event => {
    emptyErrorContainer();
    const subjectName = $("form").attr("data-edit");
    postFormData(`/subjects/edit/${subjectName}`)
})

$("#remove-subject-btn").click(event => {
    emptyErrorContainer();
    fetch(`/remove/subject/${$("form").attr("data-edit")}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        }
    })
        .then(response => response.json())
        .then(response => {
            if (response.success === true) {
                console.log("Subject removed")
                window.location.replace(`/subjects/${termNumber}`);
            } else {
                console.log("ERROR");
                console.log(response);
                $(".error-container").append(`<p>${response.message}</p>`);
            }
        })
        .catch(error => {
            console.log('Unhappy little error :(', error);
        });
})



function postFormData(path){
    const passRequirements = {}

    $(".checkbox").each((index, element) => {
        const requirementName = $(element).attr("id").split("-")[0];
        passRequirements[requirementName] = $(element).children().length !== 0;
    })

    const termNumber = parseInt($("#term-input").attr("data-term-number"))
    fetch(path, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            name: $("#subject-name").val(),
            maxPoints: $("#max-points").val(),
            rates: {
                threeZero: $("#30-grade").val(),
                threeHalf: $("#35-grade").val(),
                fourZero: $("#40-grade").val(),
                fourHalf: $("#45-grade").val(),
                fiveZero: $("#50-grade").val()
            },
            passRequirements: passRequirements,
            termNumber: termNumber
        })
    })
        .then(response => response.json())
        .then(response => {
            if (response.success === true) {
                window.location.replace(`/subjects/${termNumber}`);
            } else {
                console.log("ERROR");
                console.log(response);
                errorContainer.append(`<p>${response.message}</p>`);
            }
        })
        .catch(error => {
            console.log('Unhappy little error :(', error);
        });
}

$("#cancel-new-subject-btn").click(event => {
    window.location.replace("/subjects");
})

$(".checkbox").click(event => {
    toggleChecks(event.currentTarget);
})

function toggleChecks(targetCheckbox) {
    console.log($(targetCheckbox).children().length);
    console.log($(targetCheckbox));
    if ($(targetCheckbox).children().length === 0) {
        $(targetCheckbox).append("<i class='fas fa-check'></i>");
    } else {
        $(targetCheckbox).empty();
    }
}

termInput.click(async () => {
    await insertTermsIntoDropdown();
    termsSelector.toggleClass("invisible");
})


async function insertTermsIntoDropdown() {
    if (termsSelector.children().length === 0) {
        const termsObject = await fetchTerms();

        for (const term in termsObject) {
            termsSelector.append(`<p class="term" data-term-number=${term}>${termsObject[term]}</p>`);
        }

        $(".term").click( event => {
            termInput
                .val($(event.currentTarget).text())
                .attr("data-term-number", $(event.currentTarget).attr("data-term-number"));
            $(".terms-selector").addClass("invisible");
        })

    }
}




