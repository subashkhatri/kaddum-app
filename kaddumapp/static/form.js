function toggleSideBar() {
    const sidebar = document.getElementById("sidebar");
    const mainPanel = document.getElementById("main");
    if (sidebar?.classList.contains("shrinked")) {
      sidebar.classList.remove("shrinked");
      mainPanel?.classList.remove("shrinked-sidebar");
    } else {
      sidebar?.classList.add("shrinked");
      mainPanel?.classList.add("shrinked-sidebar");
    }
  }
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
