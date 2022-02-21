const termSelectorOptions = $(".term-selector-options");
const termNumber = $(".term-selector-container").attr("data-term-number");
const subjectSelectorContainer = $(".subject-selector-container");
const subjectName = subjectSelectorContainer.attr("data-subject-name");


$("#term-header").click(async () => {
    await insertTermsIntoSelector();
    termSelectorOptions.toggleClass("invisible");
    contentContainer.toggleClass("invisible");
    if (subjectSelectorContainer) {
        subjectSelectorContainer.toggleClass("invisible");
    }
})


$(".add-new-button").click(event => {
    const dataAddNew = $(event.currentTarget).attr("data-add-new");
    if (dataAddNew === "subject") {
        window.location.replace(`/subjects/add_new_subject`);
    } else if (dataAddNew === "tasksheet") {
        window.location.replace(`/points/add_new_tasksheet?subjectName=${subjectName}`);
    }
})


async function insertTermsIntoSelector() {
    if (termSelectorOptions.children().length === 0) {
        const termsObject = await fetchTerms();
        console.log(termsObject)
        delete termsObject[termNumber];
        console.log(termsObject)
        console.log(termNumber)

        for (const term in termsObject) {
            termSelectorOptions.append(`<p class="term" data-term-number=${term}>${termsObject[term]}</p>`);
        }

        $(".term").click(event => {
            redirectToAnotherTerm($(event.currentTarget).attr("data-term-number"));
        })

    }
}

