// firebase.js
import { initializeApp } from "https://www.gstatic.com/firebasejs/9.22.0/firebase-app.js";
import { getDatabase, ref, onValue } from "https://www.gstatic.com/firebasejs/9.22.0/firebase-database.js";

const firebaseConfig = {
    apiKey: "AIzaSyCcxGOaiiy6Dy1MybOIOxn69xab4rsOOJ0",
    authDomain: "koko-caffe.firebaseapp.com",
    databaseURL: "https://koko-caffe-default-rtdb.europe-west1.firebasedatabase.app",
    projectId: "koko-caffe",
    storageBucket: "koko-caffe.firebasestorage.app",
    messagingSenderId: "382318796715",
    appId: "1:382318796715:web:ee9f3aca9a107f86da7cee",
    measurementId: "G-B83G77QPWW"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const db = getDatabase(app);

// دالة لجلب البيانات من Firebase
function getMenuData(section, callback) {
    const menuRef = ref(db, section);
    onValue(menuRef, (snapshot) => {
        const data = snapshot.val();
        callback(data);
    });
}

// تصدير الدوال للاستخدام في الملفات الأخرى
export { db, getMenuData };
