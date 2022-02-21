const subjectSelectorOptions = $("#subject-selector-options");
const subjectHeader = $("#subject-header");


subjectHeader.click(async () => {
    await insertSubjectsIntoSelector();
    contentContainer.toggleClass("invisible");
    subjectSelectorOptions.toggleClass("invisible");
});


async function insertSubjectsIntoSelector() {
    if (subjectSelectorOptions.children().length === 0) {
        const subjectsList = await fetchSubjectsForTerm(termNumber);
        const currSubjectNameIndex = subjectsList.indexOf(subjectHeader.text());

        if (currSubjectNameIndex !== -1) {
            subjectsList.splice(currSubjectNameIndex, 1);
        }

        subjectsList.forEach(element => {
            subjectSelectorOptions.append(`<p class="subject">${element}</p>`);
        })

        $(".subject").click(event => {
            redirectToAnotherSubject($(event.currentTarget).text())
        });
    }
}

