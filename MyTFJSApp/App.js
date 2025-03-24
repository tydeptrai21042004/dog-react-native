import React, { useState } from 'react';
import { StyleSheet, Text, View, Button, Image } from 'react-native';
import * as ImagePicker from 'expo-image-picker';

export default function App() {
  const [image, setImage] = useState(null);
  const [prediction, setPrediction] = useState(null);

  const pickImage = async () => {
    // Request permission to access the media library.
    const permissionResult = await ImagePicker.requestMediaLibraryPermissionsAsync();
    if (!permissionResult.granted) {
      alert('Permission to access the image gallery is required!');
      return;
    }

    // Launch the image picker.
    const result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      allowsEditing: true,
      aspect: [1, 1],
      quality: 1,
    });

    if (!result.cancelled) {
      setImage(result.uri);
      sendImageToBackend(result.uri);
    }
  };

  const sendImageToBackend = async (uri) => {
    try {
      const formData = new FormData();
      formData.append('image', {
        uri: uri,
        name: 'photo.jpg', // You can change the filename if needed.
        type: 'image/jpeg', // Adjust type if your image is not JPEG.
      });

      // Replace 'http://<backend-server-ip>:5000' with your actual backend URL.
      const response = await fetch('http://172.29.34.17:5000/predict', {
        method: 'POST',
        body: formData,
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      const json = await response.json();
      setPrediction(json.prediction);
    } catch (error) {
      console.error('Error during inference:', error);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Image Classification</Text>
      <Button title="Pick an Image" onPress={pickImage} />
      {image && <Image source={{ uri: image }} style={styles.image} />}
      {prediction && <Text style={styles.result}>Result: {prediction}</Text>}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1, 
    backgroundColor: '#fff', 
    alignItems: 'center', 
    justifyContent: 'center',
    padding: 16,
  },
  title: {
    fontSize: 24,
    marginBottom: 10,
  },
  image: {
    width: 200, 
    height: 200, 
    marginVertical: 20,
  },
  result: {
    fontSize: 20,
    color: 'blue',
  },
});
