import { StyleSheet, View, Pressable, Alert, Image, ActivityIndicator } from 'react-native';
import { useState, useRef } from 'react';
import { CameraView, CameraType, useCameraPermissions } from 'expo-camera';
import { ThemedText } from '@/components/themed-text';
import { ThemedView } from '@/components/themed-view';
import { IconSymbol } from '@/components/ui/icon-symbol';
import * as FileSystem from 'expo-file-system';

export default function ScanScreen() {
  const [facing, setFacing] = useState<CameraType>('back');
  const [permission, requestPermission] = useCameraPermissions();
  const [capturedPhoto, setCapturedPhoto] = useState<string | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const cameraRef = useRef<CameraView>(null);

  if (!permission) {
    return (
      <ThemedView style={styles.container}>
        <ThemedText>Loading camera...</ThemedText>
      </ThemedView>
    );
  }

  if (!permission.granted) {
    return (
      <ThemedView style={styles.container}>
        <ThemedView style={styles.permissionContainer}>
          <ThemedText style={styles.message}>
            We need your permission to use the camera
          </ThemedText>
          <Pressable style={styles.permissionButton} onPress={requestPermission}>
            <ThemedText style={styles.buttonText}>Grant Permission</ThemedText>
          </Pressable>
        </ThemedView>
      </ThemedView>
    );
  }

  const toggleCameraFacing = () => {
    setFacing(current => (current === 'back' ? 'front' : 'back'));
  };

  const identifyRock = async (photoUri: string) => {
    setIsProcessing(true);
    try {
      // Option 1: Convert to base64 for direct AI API calls
      const base64 = await FileSystem.readAsStringAsync(photoUri, {
        encoding: 'base64',
      });
      
      // TODO: Send to AI API (OpenAI Vision, Google Gemini, etc.)
      // Example structure:
      // const response = await fetch('YOUR_AI_API_ENDPOINT', {
      //   method: 'POST',
      //   headers: { 'Content-Type': 'application/json' },
      //   body: JSON.stringify({
      //     image: `data:image/jpeg;base64,${base64}`,
      //     prompt: 'Identify this rock type'
      //   })
      // });
      
      // Simulate AI processing
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      Alert.alert('Rock Identified!', 'This appears to be a sedimentary rock (simulated result)');
      setCapturedPhoto(null);
    } catch (error) {
      Alert.alert('Error', 'Failed to identify rock');
    } finally {
      setIsProcessing(false);
    }
  };

  const takePicture = async () => {
    if (cameraRef.current) {
      try {
        const photo = await cameraRef.current.takePictureAsync();
        if (photo?.uri) {
          setCapturedPhoto(photo.uri);
          await identifyRock(photo.uri);
        }
      } catch (error) {
        Alert.alert('Error', 'Failed to take picture');
      }
    }
  };

  const retakePhoto = () => {
    setCapturedPhoto(null);
  };

  // Show preview and processing state
  if (capturedPhoto) {
    return (
      <ThemedView style={styles.container}>
        <Image source={{ uri: capturedPhoto }} style={styles.preview} />
        <View style={styles.previewOverlay}>
          {isProcessing ? (
            <View style={styles.processingContainer}>
              <ActivityIndicator size="large" color="#fff" />
              <ThemedText style={styles.processingText}>
                Identifying rock...
              </ThemedText>
            </View>
          ) : (
            <Pressable style={styles.retakeButton} onPress={retakePhoto}>
              <ThemedText style={styles.buttonText}>Retake</ThemedText>
            </Pressable>
          )}
        </View>
      </ThemedView>
    );
  }

  return (
    <ThemedView style={styles.container}>
      <CameraView style={styles.camera} facing={facing} ref={cameraRef}>
        <View style={styles.overlay}>
          <View style={styles.topBar}>
            <ThemedText type="title" style={styles.title}>Scan Rock</ThemedText>
          </View>
          
          <View style={styles.bottomBar}>
            <Pressable style={styles.flipButton} onPress={toggleCameraFacing}>
              <IconSymbol name="arrow.triangle.2.circlepath.camera" size={32} color="#fff" />
            </Pressable>
            
            <Pressable style={styles.captureButton} onPress={takePicture}>
              <View style={styles.captureButtonInner} />
            </Pressable>
            
            <View style={styles.flipButton} />
          </View>
        </View>
      </CameraView>
    </ThemedView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  permissionContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  message: {
    textAlign: 'center',
    marginBottom: 20,
  },
  permissionButton: {
    backgroundColor: '#007AFF',
    paddingHorizontal: 30,
    paddingVertical: 12,
    borderRadius: 8,
  },
  camera: {
    flex: 1,
  },
  overlay: {
    flex: 1,
    backgroundColor: 'transparent',
  },
  topBar: {
    paddingTop: 60,
    paddingHorizontal: 20,
    paddingBottom: 20,
  },
  title: {
    color: '#fff',
    textShadowColor: 'rgba(0, 0, 0, 0.75)',
    textShadowOffset: { width: -1, height: 1 },
    textShadowRadius: 10,
  },
  bottomBar: {
    position: 'absolute',
    bottom: 40,
    left: 0,
    right: 0,
    flexDirection: 'row',
    justifyContent: 'space-around',
    alignItems: 'center',
    paddingHorizontal: 20,
  },
  captureButton: {
    width: 70,
    height: 70,
    borderRadius: 35,
    backgroundColor: 'rgba(255, 255, 255, 0.3)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  captureButtonInner: {
    width: 60,
    height: 60,
    borderRadius: 30,
    backgroundColor: '#fff',
  },
  flipButton: {
    width: 50,
    height: 50,
    justifyContent: 'center',
    alignItems: 'center',
  },
  buttonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
  preview: {
    flex: 1,
    width: '100%',
    height: '100%',
  },
  previewOverlay: {
    position: 'absolute',
    bottom: 40,
    left: 0,
    right: 0,
    alignItems: 'center',
  },
  processingContainer: {
    alignItems: 'center',
    backgroundColor: 'rgba(0, 0, 0, 0.7)',
    padding: 20,
    borderRadius: 10,
  },
  processingText: {
    color: '#fff',
    marginTop: 10,
    fontSize: 16,
  },
  retakeButton: {
    backgroundColor: '#007AFF',
    paddingHorizontal: 40,
    paddingVertical: 15,
    borderRadius: 10,
  },
});
