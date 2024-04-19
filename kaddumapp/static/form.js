document.getElementById('date').addEventListener('change', function() {
    var input = this.value;
    var date = new Date(input);
    var days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday',
        'Thursday', 'Friday', 'Saturday'
    ];
    var dayName = days[date.getDay()];
    var select = document.getElementById('day');
    select.value = dayName;
});
