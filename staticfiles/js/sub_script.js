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
