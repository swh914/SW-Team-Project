// Firebase Admin SDK 초기화
const admin = require("firebase-admin");

// Firebase 서비스 계정 키 파일 경로
const serviceAccount = "/home/wonawanna/firebase-backup/serviceAccountKey.json";

// Firebase Admin 초기화
admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
  databaseURL: "https://sw-project-7ef51-default-rtdb.firebaseio.com" // Firebase Realtime Database URL
});

// Firebase Realtime Database에서 모든 데이터를 가져오기
const ref = admin.database().ref("/");  // 경로를 명시적으로 "/"로 설정

// Firebase에서 데이터를 읽어오기
ref.once("value", (snapshot) => {
    const data = snapshot.val();
    if (data) {
        console.log("Data retrieved:", data);
        // 데이터를 JSON 파일로 저장
        const fs = require('fs');
        const path = '/home/wonawanna/firebase-backup/firebase-backup.json'; // 파일 경로
        fs.writeFileSync(path, JSON.stringify(data, null, 2));
        console.log("Backup saved to", path);
    } else {
        console.log("No data found.");
    }

    process.exit();
});

