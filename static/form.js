
function toggleSideBar() {
  const sidebar = document.getElementById("sidebar");
  const mainPanel = document.getElementById("main");
  const logo = document.getElementById("side_bar_kaddum_logo");
  if (sidebar?.classList.contains("shrinked")) {
    logo.classList.remove("shrinked");
    sidebar.classList.remove("shrinked");
    mainPanel?.classList.remove("shrinked-sidebar");
  } else {
    logo.classList.add("shrinked");
    sidebar?.classList.add("shrinked");
    mainPanel?.classList.add("shrinked-sidebar");
  }
}


//Make messages in your Django template automatically disappear after a set amount of time
window.onload = function() {
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(alert => alert.style.display = 'none');
    }, 5000);
};


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


// Function to calculate total day rate
function calculateTotalDayRate(tbodySelector, totalDayRateSelector) {
    let totalDayRate = 0;

    document.querySelectorAll(tbodySelector + ' tr').forEach(row => {
        const rate = parseFloat(row.querySelector('.rate-input').value) || 0;
        totalDayRate += rate;
    });

    document.querySelector(totalDayRateSelector).textContent = totalDayRate.toFixed(2);
}

// Calculate totals on page load
calculateTotals('#employeeTableBody', '#total-hours-sum', '#total-amount-sum');
calculateTotalDayRate('#equipmentTableBody', '#total-day-rate');

// Recalculate totals whenever rate inputs change
document.querySelectorAll('.rate-input').forEach(input => {
    input.addEventListener('input', () => {
        calculateTotals('#employeeTableBody', '#total-hours-sum', '#total-amount-sum');
        calculateTotalDayRate('#equipmentTableBody', '#total-day-rate');
    });
});


const positionSelects = document.querySelectorAll(".position-select");
positionSelects.forEach(select => {
    select.addEventListener("change", function() {
        const employeeId = this.getAttribute("data-employee-id");
        const rateInput = document.querySelector(`input[name="rate_${employeeId}"]`);
        // Fetch the rate based on the selected position
        const positionId = this.value;
        fetch(`/get_rate/?position_id=${positionId}`)
            .then(response => response.json())
            .then(data => {
                // Update the rate input field with the fetched rate
                rateInput.value = data.rate;
            })
            .catch(error => {
                console.error('Error:', error);
            });
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

// Used for Day Tracking Sheet
