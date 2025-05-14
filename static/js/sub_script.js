console.log("Dashboard JS loaded");

const statusElement = document.getElementById('branchStatus');
const toggleButton = document.getElementById('toggleStatus');

const toggleBtn2 = document.getElementById('sidebarToggle');
const sidebar = document.getElementById('sidebar');

toggleBtn2.addEventListener('click', () => {
    sidebar.classList.toggle('active');
});

document.addEventListener('click', function (event) {
    const isClickInside = sidebar.contains(event.target) || toggleBtn2.contains(event.target);

    if (!isClickInside) {
      sidebar.classList.remove('active');
    }
});

toggleButton.addEventListener('click', () => {
  const isOpen = statusElement.classList.contains('open');

  if (isOpen) {
    statusElement.classList.remove('open');
    statusElement.classList.add('closed');
    statusElement.textContent = '🔴 Closed';
  } else {
    statusElement.classList.remove('closed');
    statusElement.classList.add('open');
    statusElement.textContent = '🟢 Open';
  }
});

    
      
const revenueCtx = document.getElementById('revenueChart').getContext('2d');
const revenueChart = new Chart(revenueCtx, {
  type: 'line',
  data: {
    labels: JSON.parse('{{ revenue_chart_labels|escapejs }}'),
    datasets: [{
      label: 'Revenue (₹)',
      data: JSON.parse('{{ revenue_chart_data|escapejs }}'),
      backgroundColor: 'rgba(62, 176, 180, 0.2)',
      borderColor: '#3EB0B4',
      borderWidth: 2,
      fill: true,
      tension: 0.4,
      pointBackgroundColor: '#3EB0B4'
    }]
  },
  options: {
    responsive: true,
    scales: {
      y: {
        beginAtZero: true
      }
    }
  }
});

// 🥧 Pie Chart
const payoutCtx = document.getElementById('payoutChart').getContext('2d');
const payoutChart = new Chart(payoutCtx, {
  type: 'pie',
  data: {
    labels: JSON.parse('{{ pie_labels|escapejs }}'),
    datasets: [{
      data: JSON.parse('{{ pie_values|escapejs }}'),
      backgroundColor: ['#3EB0B4', '#F39C12', '#E74C3C', '#8E44AD', '#1ABC9C'],
      borderWidth: 1
    }]
  },
  options: {
    responsive: true
  }
});

document.addEventListener("DOMContentLoaded", function () {
  const sidebar = document.getElementById("sidebar");
  const toggleBtn = document.getElementById("sidebarToggle");

  toggleBtn.addEventListener("click", function () {
    sidebar.classList.toggle("active"); // Toggles sidebar visibility
  });
});
