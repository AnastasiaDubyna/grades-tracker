
$("#add-new-tasksheet-btn").click(event => {
    console.log("WORKS I GUESS")
    const subjectName = $(".subject-selector-container").attr("data-subject-name");
    console.log("HERE" + subjectName)
    window.location.replace(`add_new_tasksheet?subjectName=${subjectName}`)
})


$(".points-tile").dblclick((event) => {
    window.location.replace(window.location + `/edit/${$(event.currentTarget).attr("data-tasksheet-number")}`);
})


function redirectToAnotherSubject(subject_name) {
    window.location.replace(`/points/${subject_name}`);
}

function redirectToAnotherTerm(termNumber) {
    console.log(termNumber)
    window.location.replace(`/points?term=${termNumber}`);
}