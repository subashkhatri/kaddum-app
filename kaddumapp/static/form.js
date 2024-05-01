var employeeNames = []; // This should be populated with actual data
var positions = []; // This should be populated with actual data

document.addEventListener('DOMContentLoaded', function() {
  // Initialize calculations
  initializeCalculations();
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
  console.log("Project Name:", projectName);  // Debugging output
  console.log("Date Selected:", date);        // Debugging output

  if (projectName && date) {
      fetch(`/check_day_tracking/?projectName=${encodeURIComponent(projectName)}&date=${encodeURIComponent(date)}`)
          .then(response => response.json())
          .then(data => {
              console.log("Received Data:", data);  // Debugging output
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

      const nameSelect = createDropdown('employeeName[]', [emp.name]); // assuming emp.name is valid
      row.insertCell(0).appendChild(nameSelect);

      const positionSelect = createDropdown('employeePosition[]', [emp.position]); // assuming emp.position is valid
      row.insertCell(1).appendChild(positionSelect);

      // Create input for hours with text-right alignment for the number input
      const hoursCell = row.insertCell(2);
      const hoursInput = document.createElement('input');
      hoursInput.type = 'number';
      hoursInput.className = 'form-control align-middle text-right'; // Apply text-right for numbers
      hoursInput.value = emp.total_hours;
      hoursInput.min = '0';
      hoursInput.name = 'totalHours[]';
      hoursInput.oninput = () => calculateTotal(hoursInput, rateInput, totalCell);
      hoursCell.appendChild(hoursInput);

      // Create input for rate
      const rateCell = row.insertCell(3);
      const rateInput = document.createElement('input');
      rateInput.type = 'number';
      rateInput.className = 'form-control align-middle text-right'; // Apply text-right for numbers
      rateInput.value = emp.rate;
      rateInput.step = '0.01';
      rateInput.name = 'itemRate[]';
      rateInput.oninput = () => calculateTotal(hoursInput, rateInput, totalCell);
      rateCell.appendChild(rateInput);

      // Total amount cell with text-right to align numbers
      const totalCell = row.insertCell(4);
      totalCell.className = 'align-middle text-right'; // Ensure numbers are right-aligned

      // Indigenous and Local columns, ensure text is centered
      const indigenousCell = row.insertCell(5);
      indigenousCell.innerHTML = emp.indigenous ? '⭕' : '';
      indigenousCell.className = 'align-middle text-center'; // Center text for indicators

      const localCell = row.insertCell(6);
      localCell.innerHTML = emp.local ? '⭕' : '';
      localCell.className = 'align-middle text-center'; // Center text for indicators

      // Initial calculation for total amount
      calculateTotal(hoursInput, rateInput, totalCell);
  });
}

// Function to calculate total amount dynamically
function calculateTotal(hoursInput, rateInput, totalCell) {
  const totalAmount = Number(hoursInput.value) * Number(rateInput.value);
  totalCell.textContent = `$${totalAmount.toFixed(2)}`;
  totalCell.className = 'align-middle text-right'; // Ensure alignment and text formatting
}

function initializeCalculations() {
  const rows = document.querySelectorAll('#employeeTableBody tr');
  rows.forEach(row => {
      const hoursInput = row.cells[2].querySelector('input');
      const rateInput = row.cells[3].querySelector('input');
      const totalCell = row.cells[4];

      // Ensure input fields exist before attaching events and calculating totals
      if (hoursInput && rateInput && totalCell) {
          hoursInput.oninput = () => calculateTotal(hoursInput, rateInput, totalCell);
          rateInput.oninput = () => calculateTotal(hoursInput, rateInput, totalCell);
          calculateTotal(hoursInput, rateInput, totalCell); // Initial calculation for each row
      }
  });
}

function addEmployeeRow() {
  const tbody = document.getElementById('employeeTableBody');
  const row = tbody.insertRow();

  // Name dropdown
  const nameCell = row.insertCell(0);
  const nameDropdown = createDropdown('employeeName[]', employeeNames);
  nameCell.appendChild(nameDropdown);

  // Position dropdown
  const positionCell = row.insertCell(1);
  const positionDropdown = createDropdown('employeePosition[]', positions);
  positionCell.appendChild(positionDropdown);

  // Hours input
  const hoursInput = createInput('number', 'totalHours[]', '0', 'form-control align-middle text-right');
  const hoursCell = row.insertCell(2);
  hoursCell.appendChild(hoursInput);

  // Rate input
  const rateInput = createInput('number', 'itemRate[]', '0.00', 'form-control align-middle text-right');
  const rateCell = row.insertCell(3);
  rateCell.appendChild(rateInput);

  // Total amount cell
  const totalCell = row.insertCell(4);
  totalCell.className = 'align-middle text-right';
  totalCell.textContent = '$0.00';

  // Indigenous and Local indicators
  const indigenousCell = row.insertCell(5);
  indigenousCell.className = 'align-middle text-center';
  indigenousCell.textContent = '⭕'; // Default value, make editable as needed

  const localCell = row.insertCell(6);
  localCell.className = 'align-middle text-center';
  localCell.textContent = ''; // Assuming false by default

  // Attach event listeners for dynamic calculation
  hoursInput.oninput = () => calculateTotal(hoursInput, rateInput, totalCell);
  rateInput.oninput = () => calculateTotal(hoursInput, rateInput, totalCell);

  // Initial calculation
  calculateTotal(hoursInput, rateInput, totalCell);
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

// Function to calculate total amount
function calculateTotal(hoursInput, rateInput, totalCell) {
  const totalAmount = Number(hoursInput.value) * Number(rateInput.value);
  totalCell.textContent = `$${totalAmount.toFixed(2)}`;
}

