// Hero Fate - Main JavaScript

// API base URL
const API_BASE = '';

// Utility Functions
function showToast(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.remove();
    }, 3000);
}

function showLoading(element) {
    element.classList.add('loading');
}

function hideLoading(element) {
    element.classList.remove('loading');
}

// API Functions
async function apiCall(url, method = 'GET', data = null) {
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json',
        }
    };
    
    if (data) {
        options.body = JSON.stringify(data);
    }
    
    try {
        const response = await fetch(url, options);
        const result = await response.json();
        
        if (!response.ok) {
            throw new Error(result.message || 'Something went wrong');
        }
        
        return result;
    } catch (error) {
        console.error('API Error:', error);
        showToast(error.message, 'error');
        throw error;
    }
}

// Authentication Functions
async function login(username, password) {
    try {
        const response = await apiCall('/api/login', 'POST', {
            username: username,
            password: password
        });
        
        if (response.success) {
            localStorage.setItem('username', username);
            localStorage.setItem('user_data', JSON.stringify(response.user));
            showToast('Đăng nhập thành công!');
            window.location.href = '/town';
        }
    } catch (error) {
        console.error('Login error:', error);
    }
}

async function register(username, password, gender) {
    try {
        const response = await apiCall('/api/register', 'POST', {
            username: username,
            password: password,
            gender: gender
        });
        
        if (response.success) {
            showToast('Đăng ký thành công! Vui lòng đăng nhập.');
            // Switch to login form
            document.getElementById('registerForm').style.display = 'none';
            document.getElementById('loginForm').style.display = 'block';
        }
    } catch (error) {
        console.error('Register error:', error);
    }
}

function logout() {
    localStorage.removeItem('username');
    localStorage.removeItem('user_data');
    window.location.href = '/';
}

// User Data Functions
function getUserData() {
    const userData = localStorage.getItem('user_data');
    return userData ? JSON.parse(userData) : null;
}

function updateUserData(newData) {
    localStorage.setItem('user_data', JSON.stringify(newData));
}

function calculateLevel(exp) {
    return Math.floor(exp / 100) + 1;
}

// Building Functions
async function loadBuildings() {
    try {
        const userData = getUserData();
        if (!userData) {
            window.location.href = '/';
            return;
        }
        
        const response = await apiCall('/api/buildings');
        const buildings = response.buildings;
        const userBuildings = userData.buildings || {};
        
        const container = document.getElementById('buildingsContainer');
        container.innerHTML = '';
        
        buildings.forEach(building => {
            const level = userBuildings[building.building_id] || 0;
            const buildingCard = createBuildingCard(building, level);
            container.appendChild(buildingCard);
        });
        
        // Update user info display
        updateUserInfoDisplay(userData);
        
    } catch (error) {
        console.error('Error loading buildings:', error);
    }
}

function createBuildingCard(building, level) {
    const card = document.createElement('div');
    card.className = 'building-card';
    card.onclick = () => openBuildingModal(building, level);
    
    const icon = getBuildingIcon(building.building_id);
    const levelClass = level > 0 ? 'built' : '';
    const levelText = level > 0 ? `Cấp ${level}` : 'Chưa xây';
    
    card.innerHTML = `
        <div class="building-level ${levelClass}">${levelText}</div>
        <div class="building-icon">
            <i class="${icon}"></i>
        </div>
        <div class="building-name">${building.name}</div>
        <div class="building-description">${building.description}</div>
    `;
    
    return card;
}

function getBuildingIcon(buildingId) {
    const icons = {
        'town_hall': 'fas fa-landmark',
        'inventory': 'fas fa-boxes',
        'forge': 'fas fa-hammer',
        'shop': 'fas fa-store',
        'potion': 'fas fa-flask',
        'mage_tower': 'fas fa-hat-wizard'
    };
    return icons[buildingId] || 'fas fa-building';
}

function updateUserInfoDisplay(userData) {
    const level = calculateLevel(userData.exp || 0);
    
    document.getElementById('userLevel').textContent = level;
    document.getElementById('userGold').textContent = userData.gold || 0;
    document.getElementById('userExp').textContent = userData.exp || 0;
    document.getElementById('userReputation').textContent = userData.reputation || 0;
}

// Building Modal Functions
function openBuildingModal(building, currentLevel) {
    const modal = document.getElementById('buildingModal');
    const userData = getUserData();
    
    // Special case for town_hall - go to quests page
    if (building.building_id === 'town_hall' && currentLevel > 0) {
        window.location.href = '/quests';
        return;
    }
    
    document.getElementById('modalBuildingName').textContent = building.name;
    document.getElementById('modalBuildingDescription').textContent = building.description;
    
    const upgradeInfo = document.getElementById('upgradeInfo');
    const upgradeButton = document.getElementById('upgradeButton');
    
    const nextLevel = currentLevel + 1;
    const upgradeData = building.upgrade_material[nextLevel.toString()];
    
    if (upgradeData) {
        let canUpgrade = userData.gold >= upgradeData.gold;
        let materialsList = '';
        
        upgradeData.materials.forEach(material => {
            const userItem = userData.inventory?.find(item => item.item_id === material.item_id);
            const userQuantity = userItem ? userItem.quantity : 0;
            const hasEnough = userQuantity >= material.quantity;
            canUpgrade = canUpgrade && hasEnough;
            
            const statusClass = hasEnough ? 'text-success' : 'text-danger';
            materialsList += `<div class="${statusClass}">${material.item_id}: ${userQuantity}/${material.quantity}</div>`;
        });
        
        upgradeInfo.innerHTML = `
            <h4>Nâng cấp lên cấp ${nextLevel}</h4>
            <p><i class="fas fa-coins"></i> Chi phí: ${upgradeData.gold} vàng</p>
            <div>Nguyên liệu cần:</div>
            ${materialsList}
        `;
        
        upgradeButton.style.display = 'block';
        upgradeButton.disabled = !canUpgrade;
        upgradeButton.textContent = currentLevel === 0 ? 'Xây dựng' : 'Nâng cấp';
        upgradeButton.onclick = () => upgradeBuilding(building.building_id, nextLevel, upgradeData);
    } else {
        upgradeInfo.innerHTML = '<p>Đã đạt cấp độ tối đa!</p>';
        upgradeButton.style.display = 'none';
    }
    
    modal.style.display = 'block';
}

async function upgradeBuilding(buildingId, newLevel, upgradeData) {
    try {
        const response = await apiCall('/api/upgrade-building', 'POST', {
            building_id: buildingId,
            level: newLevel,
            cost: upgradeData
        });
        
        if (response.success) {
            // Update local user data
            const userData = getUserData();
            if (!userData.buildings) userData.buildings = {};
            userData.buildings[buildingId] = newLevel;
            userData.gold -= upgradeData.gold;
            
            // Remove materials from inventory
            upgradeData.materials.forEach(material => {
                const userItem = userData.inventory.find(item => item.item_id === material.item_id);
                if (userItem) {
                    userItem.quantity -= material.quantity;
                    if (userItem.quantity <= 0) {
                        userData.inventory = userData.inventory.filter(item => item.item_id !== material.item_id);
                    }
                }
            });
            
            updateUserData(userData);
            closeModal();
            loadBuildings(); // Reload buildings display
            showToast('Nâng cấp thành công!');
        }
    } catch (error) {
        console.error('Upgrade error:', error);
    }
}

// Modal Functions
function closeModal() {
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modal => {
        modal.style.display = 'none';
    });
}

// Slideshow Functions
let currentSlide = 0;
const slides = [
    {
        image: '/static/img/background/1.jpg',
        title: 'Xây dựng thị trấn của bạn',
        description: 'Phát triển các công trình để mở khóa tính năng mới'
    },
    {
        image: '/static/img/background/2.jpg',
        title: 'Chiến đấu với quái vật',
        description: 'Sử dụng kỹ năng và chiến thuật để chiến thắng'
    },
    {
        image: '/static/img/background/3.jpg',
        title: 'Hoàn thành nhiệm vụ',
        description: 'Nhận phần thưởng và nâng cao danh tiếng'
    }
];

function initSlideshow() {
    const container = document.getElementById('slideshowContainer');
    if (!container) return;
    
    slides.forEach((slide, index) => {
        const slideElement = document.createElement('div');
        slideElement.className = `slide ${index === 0 ? 'active' : ''}`;
        slideElement.innerHTML = `
            <img src="${slide.image}" alt="${slide.title}" onerror="this.src='/static/img/background/1.jpg'">
            <div class="slide-text">
                <h3>${slide.title}</h3>
                <p>${slide.description}</p>
            </div>
        `;
        container.appendChild(slideElement);
    });
    
    // Auto advance slides
    setInterval(nextSlide, 5000);
}

function nextSlide() {
    const slideElements = document.querySelectorAll('.slide');
    if (slideElements.length === 0) return;
    
    slideElements[currentSlide].classList.remove('active');
    currentSlide = (currentSlide + 1) % slideElements.length;
    slideElements[currentSlide].classList.add('active');
}

// Form Functions
function switchForm(formType) {
    document.getElementById('loginForm').style.display = formType === 'login' ? 'block' : 'none';
    document.getElementById('registerForm').style.display = formType === 'register' ? 'block' : 'none';
}

// Event Listeners
document.addEventListener('DOMContentLoaded', function() {
    // Initialize slideshow if on index page
    initSlideshow();
    
    // Load buildings if on town page
    if (window.location.pathname === '/town') {
        loadBuildings();
    }
    
    // Close modal when clicking outside
    window.onclick = function(event) {
        const modals = document.querySelectorAll('.modal');
        modals.forEach(modal => {
            if (event.target === modal) {
                modal.style.display = 'none';
            }
        });
    };
    
    // Login form submit
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const username = document.getElementById('loginUsername').value;
            const password = document.getElementById('loginPassword').value;
            login(username, password);
        });
    }
    
    // Register form submit
    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        registerForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const username = document.getElementById('registerUsername').value;
            const password = document.getElementById('registerPassword').value;
            const gender = document.getElementById('registerGender').value;
            register(username, password, gender);
        });
    }
});
