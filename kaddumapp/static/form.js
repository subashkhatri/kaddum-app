var employeeNames = []; // This should be populated with actual data
var positions = []; // This should be populated with actual data

document.addEventListener('DOMContentLoaded', function() {
  const tbody = document.querySelector('#employeeTableBody');
  // Add event listener for input changes on rate fields
  tbody.addEventListener('input', function(event) {
    if (event.target.matches('input[name="itemRate[]"], input[name="hours[]"]')) {
      const row = event.target.closest('tr');
      updateRowTotal(row);  // Update the row total based on input
      calculateTotalAmounts();  // Recalculate the total amounts for all rows
    }
  });
  initializeCalculations();
  calculateTotalHours();
  calculateTotalAmounts();
});


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


function updateCostingFields() {
  var projectName = document.getElementById('projectName').value;
  var date = document.getElementById('date').value;
  if (projectName && date) {
      fetch(`/check_day_tracking/?projectName=${encodeURIComponent(projectName)}&date=${encodeURIComponent(date)}`)
          .then(response => response.json())
          .then(data => {
              if (data.success) {
                  updateEmployeeTable(data.employees);
              } else {
                  alert(data.message); // Notify user if no match found or any error
              }
          })
          .catch(error => {
            console.error('Error fetching data:', error);
            alert('Error fetching data: ' + error);
        });
    }
}


function updateEmployeeTable(employees) {
  const tbody = document.getElementById('employeeTableBody');
  tbody.innerHTML = ''; // Clear existing entries
  employees.forEach(emp => {
      const row = tbody.insertRow();

      const nameCell = row.insertCell(0);
      nameCell.textContent = emp.name;
      nameCell.className = 'align-middle'; 

      const positionSelect = createDropdown('employeePosition[]', [emp.position]); 
      row.insertCell(1).appendChild(positionSelect);

      // Create input for rate
      const rateCell = row.insertCell(2);
      const rateInput = document.createElement('input');
      rateInput.type = 'number';
      rateInput.className = 'form-control align-middle text-right';
      rateInput.value = emp.rate;
      rateInput.name = 'itemRate[]';
      rateCell.appendChild(rateInput);

      // Create input for hours with text-right alignment for the number input
      const hoursCell = row.insertCell(3);
      hoursCell.textContent = emp.total_hours;
      hoursCell.className = 'align-middle text-right';

      // Total amount cell with text-right to align numbers
      const totalCell = row.insertCell(4);
      totalCell.className = 'align-middle text-right'; // Ensure numbers are right-aligned

      // Ensure that hours are passed as a number
      calculateTotal(emp.total_hours, rateInput, totalCell);

      // Setup the event listener after totalCell is defined
      rateInput.oninput = () => calculateTotal(emp.total_hours, rateInput, totalCell);

      // Indigenous and Local columns, ensure text is centered
      const indigenousCell = row.insertCell(5);
      indigenousCell.innerHTML = emp.indigenous ? '⭕' : '';
      indigenousCell.className = 'align-middle text-center'; // Center text for indicators

      const localCell = row.insertCell(6);
      localCell.innerHTML = emp.local ? '⭕' : '';
      localCell.className = 'align-middle text-center'; // Center text for indicators

      // Call calculation functions after the table is populated    
      calculateTotalHours();
      calculateTotalAmounts();
  });
}


function calculateTotal(hours, rateInput, totalCell) {
  const hoursNumber = Number(hours); 
  const rateValue = Number(rateInput.value); 
  const totalAmount = hoursNumber * rateValue; 
  if (!isNaN(totalAmount)) { 
    totalCell.textContent = `$${totalAmount.toFixed(2)}`;
  } else {
    totalCell.textContent = "$0.00"; // Default to $0.00 if calculation fails
  }
  totalCell.className = 'align-middle text-right'; 
}


function initializeCalculations() {
  const rows = document.querySelectorAll('#employeeTableBody tr');
  rows.forEach(row => {
      const rateInput = row.cells[2].querySelector('input');
      const hours = row.cells[3].textContent.trim();// Trim any whitespace
      const totalCell = row.cells[4];
      // Ensure input fields exist before attaching events and calculating totals
      if (rateInput && totalCell) {          
          rateInput.oninput = () => calculateTotal(hours, rateInput, totalCell);
          calculateTotal(hours, rateInput, totalCell); // Initial calculation for each row
      }
  });
}


function createDropdown(name, options) {
  const select = document.createElement('select');
  select.name = name;
  select.className = 'form-control align-middle';
  options.forEach(option => {
    const opt = document.createElement('option');
    opt.value = option;
    opt.textContent = option;
    select.appendChild(opt);
  });
  return select;
}


function createInput(type, name, value, className) {
  const input = document.createElement('input');
  input.type = type;
  input.name = name;
  input.value = value;
  input.className = className;
  return input;
}


function calculateTotalHours() {
  const rows = document.querySelectorAll('#employeeTableBody tr');
  let totalHours = 0;
  rows.forEach((row) => {
      let hoursText = row.cells[3].textContent.trim();
      hoursText = hoursText || '0'; // Set default to '0' if empty
      const hours = parseFloat(hoursText);
      totalHours += hours;     
  });
  // Update the footer
  const footerTotalHoursCell = document.querySelector('tfoot tr td:nth-child(2)');
  footerTotalHoursCell.textContent = totalHours.toFixed(2);
}


function updateRowTotal(row) {
  const rateInput = row.querySelector('input[name="itemRate[]"]');
  if (rateInput) {
    const hoursCell = row.cells[3];
    const hours = parseFloat(hoursCell.textContent.trim() || "0");
    const rate = parseFloat(rateInput.value.trim() || "0");
    const totalCell = row.cells[4];
    const totalAmount = hours * rate;
    totalCell.textContent = `$${totalAmount.toFixed(2)}`;
    calculateTotalAmounts(); // Recalculate totals for all rows whenever a row is updated
  }
}


function calculateTotalAmounts() {
  const rows = document.querySelectorAll('#employeeTableBody tr');
  let totalAmount = 0;
  rows.forEach((row) => {
    const amountText = row.cells[4].textContent.replace('$', '').trim();
    const amount = parseFloat(amountText);
    if (!isNaN(amount)) {
      totalAmount += amount;
    }
  });
  const footerTotalAmountCell = document.querySelector('tfoot tr td:nth-child(3)');
  if (footerTotalAmountCell) {
    footerTotalAmountCell.textContent = `$${totalAmount.toFixed(2)}`;
  }
}
