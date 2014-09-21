/**
 * Created by Cartoon on 2014/9/20.
 */
function nowString() {
    now = new Date();
    y = now.getYear() + 1900;
    M = now.getMonth() + 1;
    M = (M < 10 ? '0' : '') + M;
    d = now.getDate();
    d = (d < 10 ? '0' : '') + d;
    h = now.getHours();
    h = (h < 10 ? '0' : '') + h;
    m = now.getMinutes();
    m = (m < 10 ? '0' : '') + m;
    s = now.getSeconds();
    s = (s < 10 ? '0' : '') + s;
    w = now.getDay();
    dayOfWeeks = document.getElementsByName("dayOfWeek");
    return y + "-" + M + "-" + d + " " + h + ":" + m + ":" + s + " " + dayOfWeeks[w].innerHTML
}
time_dom = null;
function show(time_id) {
    time_dom = document.getElementById(time_id);
    tick()
}

function tick() {
    time_dom.innerHTML = nowString();
    window.setTimeout("tick()", 1000);
}

show('time-div');

function render_duty() {
    $.ajax({url:'duty', method:'post', success:function(data){
        duty = data.result;
        $('#duty_time')[0].innerHTML = (duty.work_start + " --- " + duty.work_end);
        $('#duty_yesterday')[0].innerHTML = (duty.yesterday_start + " --- " + duty.yesterday_end);
        $('#check_in')[0].innerHTML = (duty.today_start)
    }})
}