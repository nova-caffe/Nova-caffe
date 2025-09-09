// js/load-menu.js - ملف تحميل البيانات الديناميكي
class MenuLoader {
    constructor() {
        this.baseUrl = 'https://nova-caffe.github.io/Nova-caffe/data';
        this.currentPage = this.getCurrentPage();
    }

    // تحديد الصفحة الحالية بناءً على اسم الملف
    getCurrentPage() {
        const path = window.location.pathname;
        if (path.includes('Drink-menu')) return 'drinks';
        if (path.includes('Food-menu')) return 'food';
        if (path.includes('shesha-menu')) return 'shesha';
        return null;
    }

    // تحميل بيانات القسم المحدد
    async loadSectionData(section) {
        try {
            const response = await fetch(`${this.baseUrl}/${this.currentPage}/${section}.json`);
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            return await response.json();
        } catch (error) {
            console.error(`Failed to load ${section}:`, error);
            return this.getDefaultData(section);
        }
    }

    // بيانات افتراضية في حالة فشل التحميل
    getDefaultData(section) {
        const defaults = {
            drinks: {
                coffee: { category: "القهوة والمشروبات الساخنة", items: [] },
                'soft-drinks': { category: "المشروبات الغازية", items: [] },
                desserts: { category: "الحلويات", items: [] },
                'cold-drinks': { category: "المشروبات الباردة", items: [] }
            },
            food: {
                'main-dishes': { category: "الوجبات الرئيسية", items: [] },
                'add-ons': { category: "الإضافات", items: [] }
            },
            shesha: {
                classic: { category: "الشيشة التقليدية", items: [] },
                premium: { category: "الشيشة المميزة", items: [] },
                'add-ons': { category: "إضافات الشيشة", items: [] }
            }
        };

        return defaults[this.currentPage]?.[section] || { category: section, items: [] };
    }

    // عرض البيانات في القسم المحدد
    async renderSection(sectionId, dataKey) {
        const sectionElement = document.getElementById(sectionId);
        if (!sectionElement) return;

        const data = await this.loadSectionData(dataKey);
        const loadingElement = sectionElement.querySelector('.loading');
        
        if (loadingElement) {
            loadingElement.remove();
        }

        // تحديث عنوان القسم
        const titleElement = sectionElement.querySelector('.section-title');
        if (titleElement && data.category) {
            titleElement.textContent = data.category;
        }

        // إنشاء قائمة العناصر
        const menuList = sectionElement.querySelector('.menu-list') || document.createElement('ul');
        if (!sectionElement.querySelector('.menu-list')) {
            menuList.className = 'menu-list';
            sectionElement.appendChild(menuList);
        } else {
            menuList.innerHTML = '';
        }

        // إضافة العناصر إلى القائمة
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

        // إضافة تأثيرات التفاعل للعناصر الجديدة
        this.addMenuInteractions();
    }

    // إضافة تأثيرات التفاعل لعناصر القائمة
    addMenuInteractions() {
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

    // تحميل جميع أقسام الصفحة
    async loadAllSections() {
        if (!this.currentPage) return;

        const sections = {
            drinks: [
                { id: 'coffee-section', key: 'coffee' },
                { id: 'soft-drinks-section', key: 'soft-drinks' },
                { id: 'desserts-section', key: 'desserts' },
                { id: 'cold-drinks-section', key: 'cold-drinks' }
            ],
            food: [
                { id: 'main-dishes-section', key: 'main-dishes' },
                { id: 'addons-section', key: 'add-ons' }
            ],
            shesha: [
                { id: 'classic-shisha-section', key: 'classic' },
                { id: 'premium-shisha-section', key: 'premium' },
                { id: 'shisha-addons-section', key: 'add-ons' }
            ]
        };

        const pageSections = sections[this.currentPage] || [];
        
        for (const section of pageSections) {
            await this.renderSection(section.id, section.key);
        }
    }

    // تهيئة المحمل
    init() {
        if (this.currentPage) {
            document.addEventListener('DOMContentLoaded', () => {
                this.loadAllSections();
            });
        }
    }
}

// تهيئة المحمل وتشغيله
const menuLoader = new MenuLoader();
menuLoader.init();

// دالة مساعدة للتحميل اليدوي من الصفحات الأخرى
window.loadMenuData = function() {
    menuLoader.loadAllSections();
};
