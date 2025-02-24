import pandas as pd
import torch
import torch.nn as nn

# Define the LSTM model architecture
class LSTMModel(nn.Module):
    def __init__(self, input_size, hidden_size, output_size, num_layers, dropout):
        super(LSTMModel, self).__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers=num_layers, dropout=dropout, batch_first=True)
        self.fc1 = nn.Linear(hidden_size, 10)
        self.fc2 = nn.Linear(10, output_size)

    def forward(self, x):
        _, (out, _) = self.lstm(x)
        out = self.fc1(out.squeeze(0))  # Squeeze the batch dimension
        out = self.fc2(out)
        return out

# Input data for prediction
input_data = {
    "priceDate": 1704412800000000000,
    "open": 236.86,
    "low": 235.5001,
    "high": 244.1196,
    "volume": 93488939.0,
    "Revenues": 23350000000,
    "NetIncomeLoss": 1853000000,
    "EarningsPerShareBasic": 0.58,
    "EarningsPerShareDiluted": 0.53,
    "OperatingIncomeLoss": 1764000000,
    "CostOfRevenue": 19172000000,
    "GrossProfit": 4178000000,
    "CashAndCashEquivalentsAtCarryingValue": 15932000000,
    "LongTermDebt": 2152000000,
    "DebtCurrent": 1552000000,
    "Assets": 93941000000,
    "LiabilitiesCurrent": 26640000000,
    "InventoryNet": 13721000000,
    "ResearchAndDevelopmentExpense": 1161000000
}

# Create a DataFrame from the input data
input_df = pd.DataFrame([input_data])

# Convert the input to a PyTorch tensor
input_tensor = torch.FloatTensor(input_df.values)

# Reshape input data to match the model's expected input shape
input_tensor = input_tensor.reshape((input_tensor.shape[0], 1, input_tensor.shape[1]))

# Initialize the model
input_size = input_tensor.shape[2]  # Assuming input_size is the number of features
hidden_size = 100  # Adjusted hidden size
output_size = 1
num_layers = 2  # Adjusted number of layers
dropout = 0.01
model = LSTMModel(input_size, hidden_size, output_size, num_layers, dropout)

# Load the trained model weights
model_filename = './models/TSLA_combined_data_pytorch.pth'
model.load_state_dict(torch.load(model_filename))
model.eval()

# Make predictions for the input data
with torch.no_grad():
    predicted_close_price = model(input_tensor)

# Display the predicted close price
print(f'Predicted Close Price: ${predicted_close_price[0, 0].item():.2f}')
