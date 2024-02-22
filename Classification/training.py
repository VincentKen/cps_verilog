import os
import torch
from typing import Tuple
import numpy as np

def calculate_mean_std(images) -> Tuple[Tuple, Tuple]:
  converted_dataset = np.array(images) / 255
  mean = tuple(np.mean(converted_dataset, axis=(0,1,2)))
  std = tuple(np.std(converted_dataset, axis=(0,1,2)))

  return mean, std

def train_loop(dataloader, model, loss_fn, optimizer, device):
  size = len(dataloader.dataset)
  num_batches = len(dataloader)
  train_loss = 0.0
  train_accuracy = 0.0
  for batch, (X, y) in enumerate(dataloader):
    # Compute prediction and loss
    out, pred = model(X.to(device))
    loss = loss_fn(pred, y.to(device))
    # Backpropagation
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    train_loss += loss.item()
    train_accuracy += (pred.argmax(1) == y.to(device)).type(torch.float).sum().item()


    if batch % 7 == 0:
      loss, current = loss.item(), batch * len(X)
      print(f"loss: {loss:>7f}  [{current:>5d}/{size:>5d}]")
      print()

  train_loss /= num_batches
  train_accuracy /= size
  return train_loss, train_accuracy


def test_loop(dataloader, model, loss_fn, device):
  size = len(dataloader.dataset)
  num_batches = len(dataloader)
  test_loss, test_accuracy = 0, 0

  with torch.no_grad():
    for X, y in dataloader:
      out, pred = model(X.to(device))
      test_loss += loss_fn(pred, y.to(device)).item()
      test_accuracy += (pred.argmax(1) == y.to(device)).type(torch.float).sum().item()

  test_loss /= num_batches
  test_accuracy /= size
  print(f"Test Error: \n Accuracy: {(100*test_accuracy):>0.1f}%, Avg loss: {test_loss:>8f} \n")
  return test_loss, test_accuracy


def start_training(epochs, trainloader, model, loss_fn, optimizer, device):
  train_losses = []
  train_accuracies = []

  test_losses = []
  test_accuracies = []

  for t in range(epochs):
    print(f"Epoch {t + 1}\n-------------------------------")
    train_loss, train_acc = train_loop(trainloader,
                                       model,
                                       loss_fn,
                                       optimizer, device)

    #test_loss, test_acc = test_loop(trainloader,
                                    #model,
                                    #loss_fn, device)

    train_losses.append(train_loss)
    train_accuracies.append(train_acc)

    #test_losses.append(test_loss)
    #test_accuracies.append(test_acc)
  torch.save(model.state_dict(), os.path.join("output_dir", 'checkpoint_%02d.pth'%epochs))
  print("Done!")