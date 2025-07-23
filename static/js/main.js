// Hero Fate - Main JavaScript

// Mobile Detection & Redirect
function isMobileDevice() {
    const userAgent = navigator.userAgent.toLowerCase();
    const mobileKeywords = ['mobile', 'android', 'iphone', 'ipad', 'ipod', 'blackberry', 'opera mini'];
    const screenWidth = window.screen.width;
    const screenHeight = window.screen.height;
    
    // Check by user agent
    const isMobileUA = mobileKeywords.some(keyword => userAgent.includes(keyword));
    
    // Check by screen size (typical mobile/tablet sizes)
    const isMobileScreen = screenWidth <= 768 || screenHeight <= 768;
    
    return isMobileUA || isMobileScreen;
}

function checkMobileAndRedirect() {
    if (isMobileDevice() && !window.location.pathname.includes('/not-implemented')) {
        window.location.href = '/not-implemented';
        return true;
    }
    return false;
}

// Run mobile check immediately
if (checkMobileAndRedirect()) {
    // Stop execution if redirecting
    throw new Error('Redirecting to mobile not-supported page');
}

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
    // Call logout API to clear session
    apiCall('/api/logout', 'POST')
        .then(response => {
            if (response.success) {
                showToast('Đăng xuất thành công!');
            }
        })
        .catch(error => {
            console.error('Logout error:', error);
        })
        .finally(() => {
            // Clear local storage and redirect regardless of API result
            localStorage.removeItem('username');
            localStorage.removeItem('user_data');
            window.location.href = '/';
        });
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
        // Get fresh user data from server
        const userResponse = await apiCall('/api/user');
        if (!userResponse.success) {
            window.location.href = '/';
            return;
        }
        
        const userData = userResponse.user;
        updateUserData(userData); // Update local storage
        
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
        window.location.href = '/';
    }
}

function createBuildingCard(building, level) {
    const card = document.createElement('div');
    card.className = `building-card ${level > 0 ? 'built' : 'not-built'}`;
    card.onclick = () => openBuildingModal(building, level);
    
    const levelClass = level > 0 ? 'built' : '';
    const levelText = level > 0 ? `Cấp ${level}` : 'Chưa xây';
    
    // URL hình ảnh công trình
    const buildingImageUrl = `/static/img/building/${building.building_id}.png`;
    
    card.innerHTML = `
        <div class="building-level ${levelClass}">${levelText}</div>
        <div class="building-image">
            <div class="building-structure" style="background-image: url('${buildingImageUrl}');"></div>
        </div>
        <div class="building-name">${building.name}</div>
        <div class="building-description">${building.description}</div>
    `;
    
    return card;
}

function getBuildingIcon(buildingId) {
    const icons = {
        'town_hall': 'fas fa-landmark',
        'storage': 'fas fa-boxes',      // Đổi từ 'inventory'
        'blacksmith': 'fas fa-hammer',  // Đổi từ 'forge'
        'market': 'fas fa-store',       // Đổi từ 'shop'
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
        image: '/static/img/background/3.jpg',
        title: 'Xây dựng thị trấn của bạn',
        description: 'Hãy cùng phát triển thị trần của bạn với các công trình để mở khóa tính năng mới.'
    },
    {
        image: '/static/img/background/2.jpg',
        title: 'Chiến đấu với quái vật',
        description: 'Hoà mình vào thế giới fantasy. Mỗi trận chiến là một thử thách. Hãy sử dụng kỹ năng và chiến thuật để dành chiến thắng..'
    },
    {
        image: '/static/img/background/1.jpg',
        title: 'Hoàn thành nhiệm vụ',
        description: 'Hành trình thú vị trong thế giới trung cổ. Làm nhiệm vụ, nhận các phần phần thưởng và nâng cao danh tiếng.'
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
    setInterval(nextSlide, 2000);
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

// Authentication Status Check
async function checkAuthStatus() {
    try {
        const response = await apiCall('/api/auth-status');
        if (response.success && response.authenticated) {
            // User is authenticated, redirect to town if on index page
            if (window.location.pathname === '/' || window.location.pathname === '/index') {
                window.location.href = '/town';
                return;
            }
            // Update local storage with fresh user data
            localStorage.setItem('username', response.user.username);
            localStorage.setItem('user_data', JSON.stringify(response.user));
        } else {
            // User not authenticated, clear local storage
            localStorage.removeItem('username');
            localStorage.removeItem('user_data');
            
            // Redirect to index if on protected pages
            if (window.location.pathname === '/town' || window.location.pathname === '/quests') {
                window.location.href = '/';
            }
        }
    } catch (error) {
        console.error('Auth status check error:', error);
        // On error, clear local storage and redirect to index if on protected pages
        localStorage.removeItem('username');
        localStorage.removeItem('user_data');
        if (window.location.pathname === '/town' || window.location.pathname === '/quests') {
            window.location.href = '/';
        }
    }
}

// Event Listeners
document.addEventListener('DOMContentLoaded', function() {
    // Check authentication status first
    checkAuthStatus();
    
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
