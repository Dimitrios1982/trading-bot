import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from sklearn.model_selection import train_test_split

ticker = "TSLA"
script_filename = "combined_data"

# Load combined_data
combined_data = pd.read_csv('./data/combined_data.csv')  # Replace with the actual path

# Drop rows with missing values
combined_data = combined_data.dropna()

# Extract features (X) and target variable (y)
features = combined_data.drop(columns=["close"]).values
target = combined_data["close"].values.reshape(-1, 1)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

# Convert data to PyTorch tensors
X_train_tensor = torch.FloatTensor(X_train)
y_train_tensor = torch.FloatTensor(y_train)
X_test_tensor = torch.FloatTensor(X_test)
y_test_tensor = torch.FloatTensor(y_test)

# Define the LSTM model
class LSTMModel(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(LSTMModel, self).__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, batch_first=True)
        self.fc1 = nn.Linear(hidden_size, 25)
        self.fc2 = nn.Linear(25, output_size)

    def forward(self, x):
        _, (out, _) = self.lstm(x)
        out = self.fc1(out.squeeze(0))  # Squeeze the batch dimension
        out = self.fc2(out)
        return out

# Initialize the model
input_size = X_train_tensor.shape[1] # Adjusted to the correct dimension for input_size
hidden_size = 50
output_size = 1
model = LSTMModel(input_size, hidden_size, output_size)

# Define loss function and optimizer
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Train the model
num_epochs = 100
for epoch in range(num_epochs):
    model.train()
    optimizer.zero_grad()
    
    outputs = model(X_train_tensor)
    loss = criterion(outputs, y_train_tensor)
    loss.backward()
    optimizer.step()

    if (epoch + 1) % 10 == 0:
        print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}')

# Evaluate the model on the test set
model.eval()
with torch.no_grad():
    test_outputs = model(X_test_tensor)
    test_loss = criterion(test_outputs, y_test_tensor)
    print(f'Mean Squared Error on Test Set: {test_loss.item():.4f}')

# Save the trained model
torch.save(model.state_dict(), f'./models/{ticker}_{script_filename}_pytorch.pth')
print(f'Model saved to ./models/{ticker}_{script_filename}_pytorch.pth')
