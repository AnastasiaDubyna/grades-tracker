const daysMapper = {
    "monday": 1,
    "tuesday": 2,
    "wednesday": 3,
    "thursday": 4,
    "friday": 5
}


$("#edit-schedule-button").click(() => {
    window.location.replace(`/schedule/edit?term=${termNumber}`);
})


$(".subject").each((index, element) => {
    const columnStart = daysMapper[$(element).attr("data-day")];
    const columnEnd = columnStart + 1;
    const rowStart = parseInt($(element).attr("data-time").split(":").shift()) - 7;
    const rowEnd = rowStart + parseInt($(element).attr("data-duration"));

    $(element).css("grid-column-start", columnStart);
    $(element).css("grid-column-end", columnEnd);
    $(element).css("grid-row-start", rowStart);
    $(element).css("grid-row-end", rowEnd);
})

const currDate = new Date();
const hour = currDate.getHours();
const minutes = currDate.getMinutes();

if (hour >=8 && hour < 20) {
    const percent = (hour - 8 + minutes/60) * 100 / 1099;
    $(".yellow-scale-line").css("height", `${percent}%`);
} else if (hour >= 20) {
    $(".yellow-scale-line").css("height", "100%");
}