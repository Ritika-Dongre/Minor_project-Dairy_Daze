const uploadInput = document.getElementById("uploadImage");
const profileImg = document.getElementById("profileImage");

uploadInput.addEventListener("change", function () {
  const file = this.files[0];
  if (file) {
    profileImg.src = URL.createObjectURL(file);
  }
});

function removeImage() {
  profileImg.src = "https://cdn-icons-png.flaticon.com/512/847/847969.png";
  uploadInput.value = "";
}

document.getElementById("editForm").addEventListener("submit", function (e) {
  e.preventDefault();
  alert("Profile saved successfully!");
});

 function toggleEditForm() {
    const display = document.getElementById('profileDisplay');
    const form = document.getElementById('editForm');
    const isVisible = form.style.display === 'block';

    display.style.display = isVisible ? 'block' : 'none';
    form.style.display = isVisible ? 'none' : 'block';
  }

  function saveProfile(event) {
    event.preventDefault();

    const name = document.getElementById('nameInput').value;
    const email = document.getElementById('emailInput').value;
    const role = document.getElementById('roleInput').value;

    document.querySelector('#profileDisplay').innerHTML = `
      <p><strong>Name:</strong> ${name}</p>
      <p><strong>Email:</strong> ${email}</p>
      <p><strong>Role:</strong> ${role}</p>
      <button class="edit-profile-btn" onclick="toggleEditForm()">Edit Profile</button>
    `;

    toggleEditForm(); // Hide form and show updated profile
  }

  document.addEventListener("DOMContentLoaded", function () {
    const toggleBtn = document.getElementById('sidebarToggle');
    const sidebar = document.getElementById('sidebar'); // safer than querySelector
  
    if (!toggleBtn || !sidebar) {
      console.error('Sidebar or toggle button not found.');
      return;
    }
  
    toggleBtn.addEventListener('click', () => {
      sidebar.classList.toggle('active');
    });
  
    document.addEventListener('click', function (event) {
      // check again if sidebar or button is null to prevent crash
      if (!sidebar || !toggleBtn) return;
  
      const isClickInside = sidebar.contains(event.target) || toggleBtn.contains(event.target);
      if (!isClickInside) {
        sidebar.classList.remove('active');
      }
    });
  });
  
  