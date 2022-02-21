$(".points-container").each((index, container) => {
    const percent = $(container).attr("data-left");
    const margin = $(container).children(":first").width() + 2;
    $(container).css("left", `calc(${percent}% - ${margin}px)`);
})

$(".scale-container").css("opacity", "1");

$(".subject-tile").dblclick(event => {
    const subjectName = $(event.currentTarget).attr("data-subject")
    window.location.replace(`/subjects/edit/${subjectName}`);
})


function redirectToAnotherTerm(termNumber) {
    console.log(termNumber)
    window.location.replace(`/subjects/${termNumber}`);
}




