import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
import torch.nn.functional as F
from torch.utils.data import DataLoader
from torchvision.datasets import ImageFolder
import matplotlib.pyplot as plt
import os
import shutil
class SimpleCNN(nn.Module):
    def __init__(self):
        super(SimpleCNN, self).__init__()
        self.conv1 = nn.Sequential(
            nn.Conv2d(in_channels=3, out_channels=16, kernel_size=5, stride=1, padding=2), 
            nn.BatchNorm2d(16),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=4)
        ) #32 16 56 56

        self.conv2 = nn.Sequential(
            nn.Conv2d(in_channels=16, out_channels=32, kernel_size=5, stride=1, padding=2),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=4)
        ) #32 32 14 14

        self.conv3 = nn.Sequential(
            nn.Conv2d(in_channels=32, out_channels=64, kernel_size=5, stride=1, padding=2),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.MaxPool2d(2)
        ) #32 64 7 7

        self.out = nn.Linear(64 * 7 * 7, 5)  # Adjusted to 5 classes

    def forward(self, x):
        x = self.conv1(x)
        x = self.conv2(x)
        x = self.conv3(x)
        x = x.view(x.size(0), -1) # output shape: (batch_size, 64 * 7 * 7)
        x = self.out(x) # output shape: (batch_size, 5)
        return x

if __name__ == '__main__':
    transform = transforms.Compose([
        transforms.Resize((224, 224)), # Resize the image to 224x224
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
    ])

    trainset = ImageFolder(root='train', transform=transform)
    trainloader = DataLoader(trainset, batch_size=32, shuffle=True, num_workers=2)

    testset = ImageFolder(root='test_add_photo', transform=transform)
    testloader = DataLoader(testset, batch_size=32, shuffle=False, num_workers=2)

    classes = trainset.classes #classed are automatically inferred from the folder structure
    print(classes)  # Ensure this prints out 5 classes

    model = SimpleCNN() # Create an instance of the SimpleCNN class

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(device)
    model.to(device) # Move the model to the GPU if available

    criterion = nn.CrossEntropyLoss() # Cross-entropy loss
    optimizer = optim.Adam(model.parameters(), lr=0.001) # Adam optimizer with learning rate of 0.001

    num_epochs = 50
    train_losses = []
    test_accuracies = []

    for epoch in range(num_epochs):
        model.train()
        running_loss = 0.0
        for i, data in enumerate(trainloader, 0):
            inputs, labels = data
            inputs, labels = inputs.to(device), labels.to(device) # Move the input and label tensors to the GPU

            # Verify the range of labels
            if not torch.all((labels >= 0) & (labels < 5)): 
                print(f"Label out of bounds detected: {labels}")
                continue

            optimizer.zero_grad() # Zero the parameter gradients
            outputs = model(inputs) # Forward pass, compute the predicted outputs by passing inputs to the model
            loss = criterion(outputs, labels) # Compute the loss
            loss.backward() # Backpropagation: compute the gradient of the loss with respect to model parameters
            optimizer.step() # Update the model's parameters based on the gradient and the learning rate

            running_loss += loss.item() # Add the loss for this mini-batch to the running total
            if i % 100 == 99:   # Print every 100 mini-batches
                print(f'Epoch {epoch + 1}, Batch {i + 1}, Loss: {running_loss / 100:.3f}')
                running_loss = 0.0

        # Append the average loss for the epoch
        train_losses.append(running_loss / len(trainloader))

        # Evaluate on test set
        model.eval() # Set the model to evaluation mode, which turns off dropout and batch normalization
        correct = 0
        total = 0 #
        with torch.no_grad(): #no need to calculate the gradients in the test phase
            for data in testloader:
                images, labels = data
                images, labels = images.to(device), labels.to(device)
                outputs = model(images)
                _, predicted = torch.max(outputs.data, 1) #max is to get the index of the max value
                total += labels.size(0)
                correct += (predicted == labels).sum().item()
                #clear the predictions folder
                if os.path.exists('predictions'):
                    shutil.rmtree('predictions')
                if num_epochs == epoch + 1: # Save the predictions only for the last epoch
                    for j in range(len(images)):
                        img_path = testloader.dataset.samples[j][0]
                        img_name = os.path.basename(img_path)
                        predicted_class = classes[predicted[j]]
                        true_class = classes[labels[j]]
                        save_dir = os.path.join('predictions', predicted_class) # Save the predictions in a folder structure
                        os.makedirs(save_dir, exist_ok=True)
                        # copy the src file to the dst folder
                        # Copy original image to prediction folder
                        shutil.copy(img_path, os.path.join(save_dir, img_name))
                        with open(os.path.join(save_dir, f"{img_name}.txt"), 'w') as f:
                            f.write(f"Predicted class: {predicted_class}\n")
                            f.write(f"Confidence: {torch.softmax(outputs[j], dim=0)[predicted[j]].item():.4f}\n")
                            f.write(f"True class: {true_class}\n")

        accuracy = 100 * correct / total
        test_accuracies.append(accuracy)
        print(f'Accuracy of the network on the test images after epoch {epoch + 1}: {accuracy}%')
    
    print('Finished Training')

    # Plot training loss
    plt.figure()
    plt.plot(train_losses, label='Training Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.title('Training Loss')
    plt.legend()
    plt.show()
    #save as train loss.png
    plt.savefig('train_loss.png')
    # Plot test accuracy
    plt.figure()
    plt.plot(test_accuracies, label='Test Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy (%)')
    plt.title('Test Accuracy')
    plt.legend()
    plt.show()
    #save as test accuracy.png
    plt.savefig('test_accuracy.png')
