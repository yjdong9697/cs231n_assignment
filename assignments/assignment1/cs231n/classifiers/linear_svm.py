from builtins import range
import numpy as np
from random import shuffle
from past.builtins import xrange


def svm_loss_naive(W, X, y, reg):
    """
    Structured SVM loss function, naive implementation (with loops).

    Inputs have dimension D, there are C classes, and we operate on minibatches
    of N examples.

    Inputs:
    - W: A numpy array of shape (D, C) containing weights. (3073 x 10)
    - X: A numpy array of shape (N, D) containing a minibatch of data. (500, 3073)
    - y: A numpy array of shape (N,) containing training labels; y[i] = c means (500)
      that X[i] has label c, where 0 <= c < C.
    - reg: (float) regularization strength

    Returns a tuple of:
    - loss as single float
    - gradient with respect to weights W; an array of same shape as W
    """
    dW = np.zeros(W.shape)  # initialize the gradient as zero
    
    # compute the loss and the gradient
    num_classes = W.shape[1]
    num_train = X.shape[0]
    dw_marginal = np.zeros((W.shape[0], W.shape[1]))
    loss = 0.0
    for i in range(num_train):
        # Dot product를 함으로써 각 pixel에 대한 클래스의 가능성이 row vector로 튀어나오게 됨
        scores = X[i].dot(W) # X[i] : i번째 input, W는 각 좌표별로 각 클래스에 대한 가중치가 저장
        correct_class_score = scores[y[i]] ## 정답 레이블에 대한 corrent score
        for j in range(num_classes):
            if j == y[i]:
                continue
            margin = scores[j] - correct_class_score + 1  # note delta = 1
            # 사실상 margin = max(0, scores[j] - corrent_class_score + 1)이랑 같은 소리
            if margin > 0:
                loss += margin
                # numpy 배열의 경우, column vector 형태로 채우는 것도 가능하다.
                dw_marginal[:, j] += X[i, :]
                dw_marginal[:,y[i]] -= X[i, :]

    # Right now the loss is a sum over all training examples, but we want it
    # to be an average instead so we divide by num_train.
    # num_train으로 전부 다 나누어주어서 총 num_train개의 input data들에 대한 loss값을 구함
    loss /= num_train

    # Add regularization to the loss.
    # 규제(릿지)
    loss += reg * np.sum(W * W)

    #############################################################################
    # TODO:                                                                     #
    # Compute the gradient of the loss function and store it dW.                #
    # Rather that first computing the loss and then computing the derivative,   #
    # it may be simpler to compute the derivative at the same time that the     #
    # loss is being computed. As a result you may need to modify some of the    #
    # code above to compute the gradient.                                       #
    #############################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    dW = dw_marginal / num_train + 2 * reg * W

    pass

    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    return loss, dW


def svm_loss_vectorized(W, X, y, reg):
    """
    Structured SVM loss function, vectorized implementation.

    Inputs and outputs are the same as svm_loss_naive.
    """
    num_train = X.shape[0]
    loss = 0.0
    dW = np.zeros(W.shape)  # initialize the gradient as zero

    #############################################################################
    # TODO:                                                                     #
    # Implement a vectorized version of the structured SVM loss, storing the    #
    # result in loss.                                                           #
    #############################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    scores = X.dot(W)
    correct_class_score = scores[np.arange(num_train), y]
    one_store = (scores + 1 > correct_class_score.reshape(-1, 1)).astype(int)
    one_store[np.arange(num_train), y] = 0

    grad_store = one_store
    grad_store[np.arange(num_train), y] -= np.sum(grad_store, axis = 1)
    
    loss = np.where(one_store == 1, scores + 1 - correct_class_score.reshape(-1, 1), 0)
    loss = np.sum(loss)
    loss /= num_train
    loss += reg * np.sum(W * W)
    pass

    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    #############################################################################
    # TODO:                                                                     #
    # Implement a vectorized version of the gradient for the structured SVM     #
    # loss, storing the result in dW.                                           #
    #                                                                           #
    # Hint: Instead of computing the gradient from scratch, it may be easier    #
    # to reuse some of the intermediate values that you used to compute the     #
    # loss.                                                                     #
    #############################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    dW = np.dot(X.T, grad_store) / num_train + 2 * reg * W

    pass

    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    return loss, dW
