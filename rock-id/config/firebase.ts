import { initializeApp } from 'firebase/app';
import { getAuth } from 'firebase/auth';
import { getFirestore } from 'firebase/firestore';
import { getStorage } from 'firebase/storage';

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyDVxgTq-PW4KRxTlljkWiV-4rz0TPqWGgM",
  authDomain: "rock-id-bb508.firebaseapp.com",
  projectId: "rock-id-bb508",
  storageBucket: "rock-id-bb508.firebasestorage.app",
  messagingSenderId: "248869863436",
  appId: "1:248869863436:ios:46ef74ff1400f949536e29"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Initialize Firebase services
export const auth = getAuth(app);
export const db = getFirestore(app);
export const storage = getStorage(app);

export default app;
