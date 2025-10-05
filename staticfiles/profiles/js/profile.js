// Profile Image Preview Functionality
/* jshint esversion: 6 */
/* global $ */

document.addEventListener('DOMContentLoaded', function() {
    const profileImageInput = document.getElementById('id_profile_image');
    const profileImageContainer = document.querySelector('.profile-image-container');
    
    if (profileImageInput) {
        profileImageInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                // Check if file is an image
                if (!file.type.startsWith('image/')) {
                    alert('Please select an image file (JPG, PNG, GIF)');
                    return;
                }
                
                // Check file size (5MB limit)
                if (file.size > 5 * 1024 * 1024) {
                    alert('File size must be less than 5MB');
                    return;
                }
                
                // Create preview
                const reader = new FileReader();
                reader.onload = function(e) {
                    const img = profileImageContainer.querySelector('img');
                    if (img) {
                        img.src = e.target.result;
                    } else {
                        // Remove placeholder and create new image
                        const placeholder = profileImageContainer.querySelector('.profile-image-placeholder');
                        if (placeholder) {
                            placeholder.remove();
                        }
                        const newImg = document.createElement('img');
                        newImg.src = e.target.result;
                        newImg.alt = 'Profile Image';
                        newImg.className = 'profile-image';
                        profileImageContainer.appendChild(newImg);
                    }
                };
                reader.readAsDataURL(file);
            }
        });
    }
    
    // Add loading animation for form submission
    const profileForm = document.getElementById('profile-form');
    if (profileForm) {
        profileForm.addEventListener('submit', function() {
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Saving...';
                submitBtn.disabled = true;
            }
        });
    }
}); 