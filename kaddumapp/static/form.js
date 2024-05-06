
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

// calculate total hours and total amount
document.addEventListener('DOMContentLoaded', function() {
  // Function to calculate totals for employees or equipment
  function calculateTotals(tbodySelector, totalHoursSelector, totalAmountSelector) {
      let totalHours = 0;
      let totalAmount = 0;

      document.querySelectorAll(tbodySelector + ' tr').forEach(row => {
          const hours = parseFloat(row.querySelector('.hours-input').textContent) || 0;
          const rate = parseFloat(row.querySelector('.rate-input').value) || 0;
          const amount = hours * rate;

          row.querySelector('.total-amount').textContent = amount.toFixed(2);

          totalHours += hours;
          totalAmount += amount;
      });

      document.querySelector(totalHoursSelector).textContent = totalHours.toFixed(2);
      document.querySelector(totalAmountSelector).textContent = totalAmount.toFixed(2);
  }

  // Calculate totals on page load
  calculateTotals('#employeeTableBody', '#total-hours-sum', '#total-amount-sum');
  calculateTotals('#equipmentTableBody', '#total-equipment-hours', '#total-equipment-amount');

  // Recalculate totals whenever rate inputs change
  document.querySelectorAll('.rate-input').forEach(input => {
      input.addEventListener('input', () => {
          calculateTotals('#employeeTableBody', '#total-hours-sum', '#total-amount-sum');
          calculateTotals('#equipmentTableBody', '#total-equipment-hours', '#total-equipment-amount');
      });
  });
});

function printPdf() {
  var printContent = document.getElementById("print-content").innerHTML;
  var originalContent = document.body.innerHTML;
  document.body.innerHTML = printContent;
  window.print();
  document.body.innerHTML = originalContent;
}