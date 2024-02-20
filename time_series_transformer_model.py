import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from einops import rearrange

ticker = "TSLA"
script_filename = "combined_data"

# Load GPU
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# Load combined_data
combined_data = pd.read_csv('./data/combined_data.csv')  # Replace with the actual path
combined_data = combined_data.dropna()

# Extract features (X) and target variable (y)
features = combined_data.drop(columns=["close"]).values
scaler_features = MinMaxScaler()
features_scaled = scaler_features.fit_transform(features)
target = combined_data["close"].values.reshape(-1, 1)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(features_scaled, target, test_size=0.2, random_state=42)

# Convert data to PyTorch tensors
X_train_tensor = torch.FloatTensor(X_train)
y_train_tensor = torch.FloatTensor(y_train)
X_test_tensor = torch.FloatTensor(X_test)
y_test_tensor = torch.FloatTensor(y_test)

# Transformer Parameters
input_size = X_train_tensor.shape[1]
d_model = X_train_tensor.shape[0]  # Model dimension
nhead = 7  # Number of attention heads
dim_feedforward = 100  # Dimension of feedforward network in Transformer encoder
num_encoder_layers = 2  # Number of encoder layers
output_size = 1

# Define the Time-Series Transformer model
class TransformerModel(nn.Module):
    def __init__(self, input_size, d_model, nhead, dim_feedforward, num_encoder_layers, output_size, dropout=0.1):
        super(TransformerModel, self).__init__()

        self.embedder = nn.Linear(input_size, d_model)
        self.pos_encoder = PositionalEncoding(d_model, dropout)
        
        encoder_layer = nn.TransformerEncoderLayer(d_model, nhead, dim_feedforward, dropout)
        self.transformer_encoder = nn.TransformerEncoder(encoder_layer, num_encoder_layers)
        
        self.decoder = nn.Linear(d_model, output_size)

    def forward(self, src):
        src = self.embedder(src) * torch.sqrt(torch.tensor(d_model))  # Embedding scaling
        src = self.pos_encoder(src)
        encoded = self.transformer_encoder(src)
        output = self.decoder(encoded)
        return output

# Positional Encoding for Transformers
class PositionalEncoding(nn.Module):
    def __init__(self, d_model, dropout=0.1):  
        super(PositionalEncoding, self).__init__()
        self.dropout = nn.Dropout(p=dropout)

    def forward(self, x):
        max_len = x.size(1)  
        pe = torch.zeros(max_len, d_model).to(device)

        # ... (The rest of your positional encoding calculation) 
        x = x + pe[:, :x.size(1)]
        return self.dropout(x)



# Initialize the model
model = TransformerModel(input_size, d_model, nhead, dim_feedforward, num_encoder_layers, output_size)
model = model.to(device) 


# Define loss function and optimizer with learning rate decay
criterion = nn.MSELoss()
learning_rate = 0.04
optimizer = optim.Adam(model.parameters(), lr=learning_rate)
scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=50, gamma=0.1)  

# Train the model
num_epochs = 500
for epoch in range(num_epochs):
    model.train()
    optimizer.zero_grad()
    X_train_tensor = X_train_tensor.to(device) # Move directly to GPU here
    y_train_tensor = y_train_tensor.to(device)
    outputs = model(X_train_tensor)
    y_train_tensor = y_train_tensor[:outputs.shape[0], :] 
    loss = criterion(outputs, y_train_tensor)
    loss.backward()
    optimizer.step()
    scheduler.step()  # Decay learning rate

    if (epoch + 1) % 10 == 0:
        print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}')

# Evaluate the model on the test set
model.eval()
with torch.no_grad():
    X_test_tensor = X_test_tensor.to(device) # Move directly to GPU here
    y_test_tensor = y_test_tensor.to(device)
    test_outputs = model(X_test_tensor)
    y_test_tensor = y_test_tensor[:test_outputs.shape[0], :]
    test_loss = criterion(test_outputs, y_test_tensor)
    print(f'Mean Squared Error on Test Set: {test_loss.item():.4f}')

# Save the trained model
torch.save(model.state_dict(), f'./models/{ticker}_{script_filename}_pytorch.pth')
print(f'Model saved to ./models/{ticker}_{script_filename}_pytorch.pth')
