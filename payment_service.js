/**
 * Payment Service - Express.js Application
 * Handles payment processing and transaction management
 */

const express = require('express');
const axios = require('axios');
const app = express();

app.use(express.json());

// Basic logging setup
const logger = {
  info: (msg) => console.log(`[INFO] ${new Date().toISOString()} - ${msg}`),
  warn: (msg) => console.warn(`[WARN] ${new Date().toISOString()} - ${msg}`),
  error: (msg) => console.error(`[ERROR] ${new Date().toISOString()} - ${msg}`)
};


/**
 * Process payment - PARTIAL LOGGING
 */
app.post('/api/payments/process', async (req, res) => {
  // Entry point has logging
  logger.info(`Processing payment for order: ${req.body.order_id}`);
  
  try {
    const { order_id, amount, payment_method, card_details } = req.body;
    
    // Validation (no logging) - GAP!
    if (!order_id || !amount || !payment_method) {
      return res.status(400).json({ error: 'Missing required fields' });
    }
    
    // CRITICAL: External payment gateway call with NO LOGGING - MAJOR GAP!
    const paymentResult = await callPaymentGateway(payment_method, amount, card_details);
    
    // Save transaction to database (no logging) - GAP!
    const transaction_id = saveTransaction(order_id, amount, paymentResult.gateway_ref);
    
    // Success logged
    logger.info(`Payment processed successfully: ${transaction_id}`);
    
    return res.status(200).json({
      transaction_id,
      status: 'success',
      gateway_ref: paymentResult.gateway_ref
    });
    
  } catch (error) {
    // Error logging present
    logger.error(`Payment processing failed: ${error.message}`);
    return res.status(500).json({ error: 'Payment processing failed' });
  }
});


/**
 * Get payment status - NO LOGGING AT ALL
 */
app.get('/api/payments/:transaction_id', async (req, res) => {
  // NO ENTRY LOGGING - GAP!
  
  try {
    // Database query with NO LOGGING - GAP!
    const payment = await getPaymentFromDB(req.params.transaction_id);
    
    if (!payment) {
      // NO ERROR LOGGING - GAP!
      return res.status(404).json({ error: 'Payment not found' });
    }
    
    // NO SUCCESS LOGGING - GAP!
    return res.status(200).json(payment);
    
  } catch (error) {
    // NO ERROR LOGGING - GAP!
    return res.status(500).json({ error: 'Failed to retrieve payment' });
  }
});


/**
 * Refund payment - MISSING CRITICAL LOGGING
 */
app.post('/api/payments/:transaction_id/refund', async (req, res) => {
  const { transaction_id } = req.params;
  const { reason } = req.body;
  
  // Entry logging present
  logger.info(`Refund requested for transaction: ${transaction_id}`);
  
  try {
    // Fetch original payment (no logging) - GAP!
    const payment = await getPaymentFromDB(transaction_id);
    
    if (!payment) {
      logger.warn(`Refund attempted for non-existent payment: ${transaction_id}`);
      return res.status(404).json({ error: 'Payment not found' });
    }
    
    // CRITICAL: External refund API call with NO LOGGING - MAJOR GAP!
    const refundResult = await processRefundWithGateway(
      payment.gateway_ref,
      payment.amount
    );
    
    // CRITICAL: Update payment status with NO LOGGING - GAP!
    await updatePaymentStatus(transaction_id, 'refunded');
    
    // NO SUCCESS LOGGING - GAP!
    return res.status(200).json({
      message: 'Refund processed',
      refund_ref: refundResult.refund_ref
    });
    
  } catch (error) {
    logger.error(`Refund failed: ${error.message}`);
    return res.status(500).json({ error: 'Refund processing failed' });
  }
});


/**
 * Verify payment - NO LOGGING
 */
app.post('/api/payments/verify', async (req, res) => {
  // NO LOGGING ANYWHERE - GAP!
  const { transaction_id, order_id } = req.body;
  
  try {
    const payment = await getPaymentFromDB(transaction_id);
    const isValid = payment && payment.order_id === order_id && payment.status === 'success';
    
    return res.status(200).json({ valid: isValid });
  } catch (error) {
    return res.status(500).json({ error: 'Verification failed' });
  }
});


/**
 * Get payment history for order - PARTIAL LOGGING
 */
app.get('/api/payments/order/:order_id', async (req, res) => {
  logger.info(`Fetching payment history for order: ${req.params.order_id}`);
  
  try {
    // Database query with NO LOGGING - GAP!
    const payments = await getPaymentsByOrderID(req.params.order_id);
    
    // NO SUCCESS LOGGING - GAP!
    return res.status(200).json({ payments, count: payments.length });
    
  } catch (error) {
    logger.error(`Failed to fetch payment history: ${error.message}`);
    return res.status(500).json({ error: 'Failed to retrieve payments' });
  }
});


/**
 * Call external payment gateway - NO LOGGING
 */
async function callPaymentGateway(paymentMethod, amount, cardDetails) {
  // CRITICAL: External API call with NO LOGGING - MAJOR GAP!
  // No request logging, no response logging, no error logging
  
  try {
    const response = await axios.post('https://payment-gateway.example.com/api/charge', {
      method: paymentMethod,
      amount: amount,
      card: cardDetails,
      currency: 'USD'
    }, {
      headers: {
        'Authorization': `Bearer ${process.env.GATEWAY_API_KEY}`,
        'Content-Type': 'application/json'
      },
      timeout: 30000
    });
    
    // NO RESPONSE LOGGING - GAP!
    return {
      success: true,
      gateway_ref: response.data.reference_id
    };
    
  } catch (error) {
    // NO ERROR DETAILS LOGGED - GAP!
    throw new Error('Payment gateway error');
  }
}


/**
 * Process refund with gateway - NO LOGGING
 */
async function processRefundWithGateway(gatewayRef, amount) {
  // CRITICAL: External refund API call with NO LOGGING - MAJOR GAP!
  
  try {
    const response = await axios.post('https://payment-gateway.example.com/api/refund', {
      reference_id: gatewayRef,
      amount: amount
    }, {
      headers: {
        'Authorization': `Bearer ${process.env.GATEWAY_API_KEY}`
      },
      timeout: 30000
    });
    
    return {
      success: true,
      refund_ref: response.data.refund_id
    };
    
  } catch (error) {
    // NO ERROR LOGGING - GAP!
    throw new Error('Refund failed');
  }
}


/**
 * Save transaction to database - NO LOGGING
 */
function saveTransaction(orderId, amount, gatewayRef) {
  // CRITICAL: Database write with NO LOGGING - MAJOR GAP!
  const transaction_id = `txn_${Date.now()}_${Math.random()}`;
  
  // Simulated database save
  // NO LOGGING OF WHAT WAS SAVED - GAP!
  
  return transaction_id;
}


/**
 * Get payment from database - NO LOGGING
 */
async function getPaymentFromDB(transactionId) {
  // Database read with NO LOGGING - GAP!
  return {
    transaction_id: transactionId,
    order_id: 'order_123',
    amount: 99.99,
    status: 'success',
    gateway_ref: 'gw_ref_123'
  };
}


/**
 * Update payment status - NO LOGGING
 */
async function updatePaymentStatus(transactionId, newStatus) {
  // CRITICAL: Status change with NO LOGGING - GAP!
  // This is important for audit trails
}


/**
 * Get payments by order ID - NO LOGGING
 */
async function getPaymentsByOrderID(orderId) {
  // Database query with NO LOGGING - GAP!
  return [];
}


/**
 * Webhook for payment gateway notifications - NO LOGGING
 */
app.post('/api/payments/webhook', (req, res) => {
  // CRITICAL: Webhook with NO LOGGING - MAJOR GAP!
  // Should log all webhook events for debugging and auditing
  
  const { event_type, transaction_id, status } = req.body;
  
  // Process webhook (no logging) - GAP!
  if (event_type === 'payment.success') {
    updatePaymentStatus(transaction_id, 'confirmed');
  } else if (event_type === 'payment.failed') {
    updatePaymentStatus(transaction_id, 'failed');
  }
  
  // NO LOGGING OF WEBHOOK PROCESSING - GAP!
  res.status(200).json({ received: true });
});


/**
 * Health check endpoint - HAS LOGGING
 */
app.get('/health', (req, res) => {
  logger.info('Health check performed');
  res.status(200).json({ status: 'healthy', service: 'payment-service' });
});


// Error handler middleware - PARTIAL LOGGING
app.use((err, req, res, next) => {
  // Has error logging
  logger.error(`Unhandled error: ${err.message}`);
  
  // But doesn't log request details - GAP!
  res.status(500).json({ error: 'Internal server error' });
});


// Start server
const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
  logger.info(`Payment Service started on port ${PORT}`);
});


module.exports = app;
