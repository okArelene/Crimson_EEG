import matplotlib.pyplot as plt
import numpy as np

# ====function setup====
def packet_decode(packets): # Decoding packets
    # Create data lists and datapoint indices for data storage
    small_packet_data = []
    big_packet_data = []
    i = 0
    # Iterate through every byte entry in the txt file
    for byte in packets:
        if i == len(packets) - 1: # Exit iteration after reaching last byte
            break
        if byte == 'AA': # Packet starting byte
            if packets[i + 1] == 'AA': # Confirm following byte
                if file_contents[i + 2] == '04': # Small packet
                    # Data storage and conversion from base 16 to base 10
                    xxHigh, xxLow, xxCheckSum = int(packets[i + 5], 16), int(packets[i + 6], 16), int(packets[i + 7], 16)
                    # Calculation for rawdata and storage
                    rawdata = (xxHigh << 8) | xxLow
                    if (rawdata > 32768):
                        rawdata -= 65536
                    small_packet_data.append(rawdata)
                elif file_contents[i + 2] == '20': # Big packet
                    # Data storage and conversion from base 16 to base 10
                    Delta = int((packets[i+7] + packets[i+8] + packets[i+9]), 16)
                    Theta = int((packets[i+10] + packets[i+11] + packets[i+12]), 16)
                    LowAlpha = int((packets[i+13] + packets[i+14] + packets[i+15]), 16)
                    HighAlpha = int((packets[i+16] + packets[i+17] + packets[i+18]), 16)
                    LowBeta = int((packets[i+19] + packets[i+20] + packets[i+21]), 16)
                    HighBeta = int((packets[i+22] + packets[i+23] + packets[i+24]), 16)
                    LowGamma = int((packets[i+25] + packets[i+26] + packets[i+27]), 16)
                    MiddleGamma = int((packets[i+28] + packets[i+29] + packets[i+30]), 16)
                    Attention = int(packets[i+32], 16)
                    Meditation = int(packets[i+34], 16)
                    big_packet = {'Delta': Delta, 'Theta': Theta, 'LowAlpha': LowAlpha, 'HighAlpha': HighAlpha, 'LowBeta': LowBeta, 'HighBeta': HighBeta, 'LowGamma': LowGamma, 'MiddleGamma': MiddleGamma, 'Attention': Attention, 'Meditation': Meditation}
                    big_packet_data.append(big_packet)
        i += 1 # Move to next byte
    return small_packet_data, big_packet_data #return final values


def graphing(small_packet_data, big_packet_data): # Plotting
    # Calculate x-axis indices for small packet data
    small_packet_indices = np.arange(len(small_packet_data))

    # Calculate x-axis indices for big packet data (every 512 small packets)
    big_packet_indices = np.arange(0, len(small_packet_data), 512)

    # Extract values from big packet data for plotting
    delta_values = [packet['Delta'] for packet in big_packet_data]
    theta_values = [packet['Theta'] for packet in big_packet_data]
    low_alpha_values = [packet['LowAlpha'] for packet in big_packet_data]
    high_alpha_values = [packet['HighAlpha'] for packet in big_packet_data]
    low_beta_values = [packet['LowBeta'] for packet in big_packet_data]
    high_beta_values = [packet['HighBeta'] for packet in big_packet_data]
    low_gamma_values = [packet['LowGamma'] for packet in big_packet_data]
    middle_gamma_values = [packet['MiddleGamma'] for packet in big_packet_data]
    attention_values = [packet['Attention'] for packet in big_packet_data]
    meditation_values = [packet['Meditation'] for packet in big_packet_data]

    # Create the figure and axes
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(15, 15), gridspec_kw={'height_ratios': [2, 1, 1]})

    # Plot the small packet data on the first subplot, centered around y=0
    ax1.plot(small_packet_indices, small_packet_data, color='brown', label='rawdata')
    ax1.axhline(0, color='black', linewidth=0.5)  # Add a horizontal line at y=0
    ax1.set_ylabel('Value')
    ax1.set_title('Small Packet Data')
    ax1.grid(True)
    ax1.legend(loc='upper right')

    # Plot the big packet data components as filled areas on the second subplot
    ax2.fill_between(big_packet_indices, delta_values, label='Delta', alpha=0.5)
    ax2.fill_between(big_packet_indices, theta_values, label='Theta', alpha=0.5)
    ax2.fill_between(big_packet_indices, low_alpha_values, label='Low Alpha', alpha=0.5)
    ax2.fill_between(big_packet_indices, high_alpha_values, label='High Alpha', alpha=0.5)
    ax2.fill_between(big_packet_indices, low_beta_values, label='Low Beta', alpha=0.5)
    ax2.fill_between(big_packet_indices, high_beta_values, label='High Beta', alpha=0.5)
    ax2.fill_between(big_packet_indices, low_gamma_values, label='Low Gamma', alpha=0.5)
    ax2.fill_between(big_packet_indices, middle_gamma_values, label='Middle Gamma', alpha=0.5)
    ax2.set_ylabel('EEG Component Values')
    ax2.set_title('Big Packet Data Components')
    ax2.grid(True)
    ax2.legend(loc='upper right')

    # Plot the attention and meditation values as a line plot on the third subplot
    ax3.fill_between(big_packet_indices, attention_values, label='Attention', alpha=0.5, color='blue')
    ax3.fill_between(big_packet_indices, meditation_values, label='Meditation', alpha=0.5, color='green')
    ax3.set_ylabel('Attention / Meditation')
    ax3.set_xlabel('Time (packets)')
    ax3.set_title('Attention and Meditation')
    ax3.grid(True)
    ax3.legend(loc='upper right')

    # Adjust the layout to reduce space between plots
    plt.tight_layout()

    # Display the plot
    plt.show()

# ====main====
# File read and data storage+setup
f = open('session.txt', 'r')
file_contents = f.readlines()[0]
file_contents = file_contents.strip(' ').split(' ')
Byte_cnt = len(file_contents)
Byte_cnt = (Byte_cnt // 8)*8
file_contents = file_contents[:Byte_cnt]

# Decode packets and storage of corresponding data lists
decoded_packets = packet_decode(file_contents)
small_packets = decoded_packets[0]
big_packets = decoded_packets[1]

# Print in terminal for data read and decode confirmation
print(small_packets)
print(big_packets)

# Graphing packet data
graphing(small_packets, big_packets)