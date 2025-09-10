// قاعدة URL للبيانات
const baseUrl = 'https://nova-caffe.github.io/Nova-caffe/data';

// دالة تحميل البيانات من JSON
async function loadJsonData(url) {
    try {
        const response = await fetch(url);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        return await response.json();
    } catch (error) {
        console.error('Failed to load data:', error);
        return null;
    }
}

// دالة عرض البيانات في القسم
function renderSection(sectionId, data) {
    const section = document.getElementById(sectionId);
    if (!section || !data) return;

    // إزالة رسالة التحميل
    const loadingElement = section.querySelector('.loading');
    if (loadingElement) {
        loadingElement.remove();
    }

    // تحديث عنوان القسم
    const titleElement = section.querySelector('.section-title');
    if (titleElement && data.category) {
        titleElement.textContent = data.category;
    }

    // إنشاء قائمة العناصر
    const menuList = section.querySelector('.menu-list') || document.createElement('ul');
    if (!section.querySelector('.menu-list')) {
        menuList.className = 'menu-list';
        section.appendChild(menuList);
    } else {
        menuList.innerHTML = '';
    }

    // إضافة العناصر إلى القائمة
    if (data.items && data.items.length > 0) {
        data.items.forEach(item => {
            const listItem = document.createElement('li');
            listItem.className = 'menu-item';
            
            listItem.innerHTML = `
                <span class="item-name">
                    ${item.icon ? `<i class="${item.icon}"></i>` : ''}
                    <span data-ar="${item.name}" data-en="${item.nameEn || item.name}">${item.name}</span>
                </span>
                <span class="item-price">${item.price}</span>
            `;

            menuList.appendChild(listItem);
        });
    }

    // إضافة تأثيرات التفاعل
    addMenuInteractions();
}

// إضافة تأثيرات التفاعل
function addMenuInteractions() {
    const menuItems = document.querySelectorAll('.menu-item');
    menuItems.forEach(item => {
        item.addEventListener('mouseenter', function() {
            this.style.backgroundColor = 'rgba(212, 175, 55, 0.15)';
            this.style.transform = 'translateX(10px)';
            this.style.transition = 'all 0.3s ease';
            this.style.borderLeft = '4px solid var(--primary-color)';
            this.style.paddingLeft = '10px';
        });

        item.addEventListener('mouseleave', function() {
            this.style.backgroundColor = 'transparent';
            this.style.transform = 'translateX(0)';
            this.style.borderLeft = 'none';
            this.style.paddingLeft = '0';
        });
    });
}

// تحميل قائمة المشروبات
async function loadDrinksMenu() {
    const sections = [
        { id: 'coffee-section', url: `${baseUrl}/drinks/coffee.json` },
        { id: 'soft-drinks-section', url: `${baseUrl}/drinks/soft-drinks.json` },
        { id: 'desserts-section', url: `${baseUrl}/drinks/desserts.json` },
        { id: 'cold-drinks-section', url: `${baseUrl}/drinks/cold-drinks.json` }
    ];

    for (const section of sections) {
        const data = await loadJsonData(section.url);
        renderSection(section.id, data);
    }
}

// تحميل قائمة الطعام
async function loadFoodMenu() {
    const sections = [
        { id: 'main-dishes-section', url: `${baseUrl}/food/main-dishes.json` },
        { id: 'addons-section', url: `${baseUrl}/food/add-ons.json` }
    ];

    for (const section of sections) {
        const data = await loadJsonData(section.url);
        renderSection(section.id, data);
    }
}

// تحميل قائمة الشيشة
async function loadSheshaMenu() {
    const sections = [
        { id: 'classic-shisha-section', url: `${baseUrl}/shesha/classic.json` },
        { id: 'premium-shisha-section', url: `${baseUrl}/shesha/premium.json` },
        { id: 'shisha-addons-section', url: `${baseUrl}/shesha/add-ons.json` }
    ];

    for (const section of sections) {
        const data = await loadJsonData(section.url);
        renderSection(section.id, data);
    }
}

// جعل الدوال متاحة globally
window.loadDrinksMenu = loadDrinksMenu;
window.loadFoodMenu = loadFoodMenu;
window.loadSheshaMenu = loadSheshaMenu;
