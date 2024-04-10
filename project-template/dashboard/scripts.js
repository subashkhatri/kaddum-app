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