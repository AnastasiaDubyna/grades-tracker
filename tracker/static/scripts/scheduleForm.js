const form =  $("form");
const formContainer = $(".form-container");
const messageContainer = $(".message-container");

$(".subject-name").click(async (event) => {
    $("input").val("");
    messageContainer.empty();
    const schedule = await fetchSubjectSchedule($(event.currentTarget).text());
    for (const subjectType in schedule) {
        console.log(subjectType)
        console.log(schedule[subjectType]["time"])
        console.log(schedule[subjectType])
        $(`#${subjectType}-day-name`).val(schedule[subjectType]["day"]);
        $(`#${subjectType}-time`).val(schedule[subjectType]["time"]);
        $(`#${subjectType}-duration`).val(schedule[subjectType]["duration"]);
    }
    form.attr("data-subject-name", $(event.currentTarget).text())
    formContainer.css("opacity", "1");
})

$("#submit-schedule-button").click(() => {
    postScheduleData(`/schedule/edit?subjectName=${form.attr("data-subject-name")}`);
})

function fetchSubjectSchedule(subjectName) {
    return fetch(`/get_schedule?subjectName=${subjectName}`, {
        method: "GET",
        headers: {
            "Content-Type": "application/json"
        }
    })
        .then(response => response.json())
        .then(response => {
            return response;
        })
        .catch(error => {
            console.log('Unhappy little error :(', error);
        });
}

function postScheduleData(path) {
    fetch(path, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            lecture: {
                day: $("#lecture-day-name").val(),
                time: $("#lecture-time").val(),
                duration: $("#lecture-duration").val()
            },
            exercise_session: {
                day: $("#exercise_session-day-name").val(),
                time: $("#exercise_session-time").val(),
                duration: $("#exercise_session-duration").val()
            },
            lab: {
                day: $("#lab-day-name").val(),
                time: $("#lab-time").val(),
                duration: $("#lab-duration").val()
            }
        })
    })
        .then(response => response.json())
        .then(response => {
            $(".message-container").append(`<p>${response.message}</p>`);
        })
        .catch(error => {
            console.log('Unhappy little error :(', error);
        });
}