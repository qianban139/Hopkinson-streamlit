"""
AI算法模型模块
包含LSTM预测模型和GAN波形生成模型
"""
import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras.models import Model, Sequential
from keras.layers import Dense, LSTM, Conv1D, Flatten, Dropout, BatchNormalization, LeakyReLU, Reshape, Input
from keras.optimizers import Adam
from typing import Tuple, Dict, List, Optional
import warnings
warnings.filterwarnings('ignore')

# ==================== LSTM预测模型 ====================
class LSTMPredictor:
    """LSTM时序预测模型"""
    
    def __init__(self, sequence_length: int = 50, prediction_horizon: int = 10):
        """
        初始化LSTM预测器
        
        Args:
            sequence_length: 输入序列长度
            prediction_horizon: 预测时长
        """
        self.sequence_length = sequence_length
        self.prediction_horizon = prediction_horizon
        self.model = None
        self.is_trained = False
        self.history = None
        
    def build_model(self, input_shape: Tuple[int, int], 
                   lstm_units: List[int] = [128, 64, 32],
                   dropout_rate: float = 0.3) -> Sequential:
        """构建LSTM预测模型
        
        Args:
            input_shape: 输入数据形状
            lstm_units: LSTM层单元数列表
            dropout_rate: Dropout比率
            
        Returns:
            构建好的模型
        """
        model = Sequential()
        
        # 第一层LSTM
        model.add(LSTM(lstm_units[0], return_sequences=True, 
                      input_shape=input_shape,
                      recurrent_dropout=0.2))
        model.add(Dropout(dropout_rate))
        
        # 中间LSTM层
        for units in lstm_units[1:-1]:
            model.add(LSTM(units, return_sequences=True, recurrent_dropout=0.2))
            model.add(Dropout(dropout_rate))
        
        # 最后一层LSTM
        model.add(LSTM(lstm_units[-1], recurrent_dropout=0.2))
        model.add(Dropout(dropout_rate))
        
        # 全连接层
        model.add(Dense(64, activation='relu'))
        model.add(Dropout(dropout_rate * 0.7))
        model.add(Dense(self.prediction_horizon, activation='linear'))
        
        # 编译模型
        model.compile(
            optimizer=Adam(learning_rate=0.001),
            loss='mse',
            metrics=['mae']
        )
        
        self.model = model
        return model
    
    def prepare_sequences(self, data: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """准备训练数据序列
        
        Args:
            data: 原始数据
            
        Returns:
            X, y 训练数据对
        """
        X, y = [], []
        for i in range(len(data) - self.sequence_length - self.prediction_horizon + 1):
            X.append(data[i:(i + self.sequence_length)])
            y.append(data[i + self.sequence_length:i + self.sequence_length + self.prediction_horizon])
        return np.array(X), np.array(y)
    
    def train(self, train_data: np.ndarray, 
              val_data: Optional[np.ndarray] = None,
              epochs: int = 100, 
              batch_size: int = 32,
              verbose: int = 0) -> Dict:
        """训练LSTM模型
        
        Args:
            train_data: 训练数据
            val_data: 验证数据
            epochs: 训练轮数
            batch_size: 批次大小
            verbose: 输出详细程度
            
        Returns:
            训练历史
        """
        X_train, y_train = self.prepare_sequences(train_data)
        
        validation_data = None
        if val_data is not None:
            X_val, y_val = self.prepare_sequences(val_data)
            validation_data = (X_val, y_val)
        
        # 添加早停和学习率调整
        callbacks = [
            keras.callbacks.EarlyStopping(patience=10, restore_best_weights=True),
            keras.callbacks.ReduceLROnPlateau(factor=0.5, patience=5, min_lr=1e-6)
        ]
        
        self.history = self.model.fit(
            X_train, y_train,
            batch_size=batch_size,
            epochs=epochs,
            validation_data=validation_data,
            callbacks=callbacks,
            verbose=verbose,
            shuffle=True
        )
        
        self.is_trained = True
        return {
            'loss': self.history.history['loss'],
            'val_loss': self.history.history.get('val_loss', []),
            'mae': self.history.history['mae'],
            'val_mae': self.history.history.get('val_mae', [])
        }
    
    def predict(self, sequence: np.ndarray) -> np.ndarray:
        """进行预测
        
        Args:
            sequence: 输入序列
            
        Returns:
            预测结果
        """
        if not self.is_trained:
            raise ValueError("模型尚未训练")
        
        if len(sequence) != self.sequence_length:
            raise ValueError(f"输入序列长度必须为{self.sequence_length}")
        
        sequence = sequence.reshape(1, self.sequence_length, -1)
        prediction = self.model.predict(sequence, verbose=0)
        return prediction.flatten()
    
    def real_time_predict(self, data_stream: np.ndarray, 
                         window_size: int = 10) -> np.ndarray:
        """实时预测方法
        
        Args:
            data_stream: 数据流
            window_size: 窗口大小
            
        Returns:
            预测结果序列
        """
        predictions = []
        for i in range(len(data_stream) - self.sequence_length - window_size + 1):
            current_sequence = data_stream[i:i + self.sequence_length]
            pred = self.predict(current_sequence)
            predictions.append(pred)
        return np.array(predictions)
    
    def evaluate(self, test_data: np.ndarray) -> Dict:
        """评估模型性能
        
        Args:
            test_data: 测试数据
            
        Returns:
            评估指标
        """
        X_test, y_test = self.prepare_sequences(test_data)
        loss, mae = self.model.evaluate(X_test, y_test, verbose=0)
        
        # 计算R²
        predictions = self.model.predict(X_test, verbose=0)
        ss_res = np.sum((y_test - predictions) ** 2)
        ss_tot = np.sum((y_test - np.mean(y_test)) ** 2)
        r2 = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0
        
        return {
            'loss': loss,
            'mae': mae,
            'r2': r2
        }

# ==================== GAN波形生成模型 ====================
class WaveformGAN:
    """GAN波形生成模型"""
    
    def __init__(self, waveform_length: int = 100, latent_dim: int = 100):
        """
        初始化GAN模型
        
        Args:
            waveform_length: 波形长度
            latent_dim: 潜空间维度
        """
        self.waveform_length = waveform_length
        self.latent_dim = latent_dim
        self.generator = None
        self.discriminator = None
        self.gan = None
        
    def build_generator(self, hidden_units: List[int] = [128, 256, 512]) -> Model:
        """构建生成器模型
        
        Args:
            hidden_units: 隐藏层单元数
            
        Returns:
            生成器模型
        """
        model = Sequential()
        
        # 输入层
        model.add(Dense(hidden_units[0], input_dim=self.latent_dim))
        model.add(LeakyReLU(alpha=0.2))
        model.add(BatchNormalization(momentum=0.8))
        
        # 隐藏层
        for units in hidden_units[1:]:
            model.add(Dense(units))
            model.add(LeakyReLU(alpha=0.2))
            model.add(BatchNormalization(momentum=0.8))
        
        # 输出层
        model.add(Dense(self.waveform_length, activation='tanh'))
        model.add(Reshape((self.waveform_length, 1)))
        
        noise = Input(shape=(self.latent_dim,))
        waveform = model(noise)
        
        return Model(noise, waveform)
    
    def build_discriminator(self, filters: List[int] = [64, 128, 256]) -> Model:
        """构建判别器模型
        
        Args:
            filters: 卷积层滤波器数量
            
        Returns:
            判别器模型
        """
        model = Sequential()
        
        # 卷积层
        for i, filt in enumerate(filters):
            if i == 0:
                model.add(Conv1D(filt, kernel_size=3, strides=2, 
                               input_shape=(self.waveform_length, 1), 
                               padding="same"))
            else:
                model.add(Conv1D(filt, kernel_size=3, strides=2, padding="same"))
            model.add(LeakyReLU(alpha=0.2))
            model.add(Dropout(0.25))
        
        # 输出层
        model.add(Flatten())
        model.add(Dense(1, activation='sigmoid'))
        
        waveform = Input(shape=(self.waveform_length, 1))
        validity = model(waveform)
        
        return Model(waveform, validity)
    
    def build_gan(self) -> Model:
        """构建完整的GAN模型
        
        Returns:
            GAN模型
        """
        # 编译判别器
        self.discriminator = self.build_discriminator()
        self.discriminator.compile(
            loss='binary_crossentropy',
            optimizer=Adam(0.0002, 0.5),
            metrics=['accuracy']
        )
        
        # 构建生成器
        self.generator = self.build_generator()
        
        # 固定判别器权重，训练生成器
        self.discriminator.trainable = False
        
        # GAN模型
        z = Input(shape=(self.latent_dim,))
        waveform = self.generator(z)
        validity = self.discriminator(waveform)
        
        self.gan = Model(z, validity)
        self.gan.compile(
            loss='binary_crossentropy',
            optimizer=Adam(0.0002, 0.5)
        )
        
        return self.gan
    
    def train(self, real_waveforms: np.ndarray, 
              epochs: int = 10000, 
              batch_size: int = 32, 
              save_interval: int = 1000,
              verbose: int = 0) -> Dict:
        """训练GAN模型
        
        Args:
            real_waveforms: 真实波形数据
            epochs: 训练轮数
            batch_size: 批次大小
            save_interval: 保存间隔
            verbose: 输出详细程度
            
        Returns:
            训练历史
        """
        real_waveforms = real_waveforms.reshape(-1, self.waveform_length, 1)
        valid = np.ones((batch_size, 1))
        fake = np.zeros((batch_size, 1))
        
        d_losses = []
        g_losses = []
        
        for epoch in range(epochs):
            # 训练判别器
            idx = np.random.randint(0, real_waveforms.shape[0], batch_size)
            real_waves = real_waveforms[idx]
            
            noise = np.random.normal(0, 1, (batch_size, self.latent_dim))
            fake_waves = self.generator.predict(noise, verbose=0)
            
            d_loss_real = self.discriminator.train_on_batch(real_waves, valid)
            d_loss_fake = self.discriminator.train_on_batch(fake_waves, fake)
            d_loss = 0.5 * np.add(d_loss_real, d_loss_fake)
            
            # 训练生成器
            noise = np.random.normal(0, 1, (batch_size, self.latent_dim))
            g_loss = self.gan.train_on_batch(noise, valid)
            
            d_losses.append(d_loss[0])
            g_losses.append(g_loss)
            
            if verbose > 0 and epoch % save_interval == 0:
                print(f"{epoch} [D loss: {d_loss[0]:.4f}, acc.: {100*d_loss[1]:.2f}%] "
                      f"[G loss: {g_loss:.4f}]")
        
        return {
            'd_losses': d_losses,
            'g_losses': g_losses
        }
    
    def generate_waveform(self, num_samples: int = 1) -> np.ndarray:
        """生成新的波形
        
        Args:
            num_samples: 生成样本数
            
        Returns:
            生成的波形
        """
        noise = np.random.normal(0, 1, (num_samples, self.latent_dim))
        generated_waves = self.generator.predict(noise, verbose=0)
        return generated_waves.reshape(num_samples, -1)
    
    def adaptive_waveform_control(self, target_specs: Dict, 
                                  num_candidates: int = 100) -> np.ndarray:
        """自适应波形调控
        
        Args:
            target_specs: 目标规格
            num_candidates: 候选波形数量
            
        Returns:
            最优波形
        """
        candidates = self.generate_waveform(num_candidates)
        
        scores = []
        for wave in candidates:
            score = self._evaluate_waveform(wave, target_specs)
            scores.append(score)
        
        best_idx = np.argmax(scores)
        return candidates[best_idx]
    
    def _evaluate_waveform(self, waveform: np.ndarray, 
                          target_specs: Dict) -> float:
        """评估波形质量
        
        Args:
            waveform: 波形数据
            target_specs: 目标规格
            
        Returns:
            评分
        """
        score = 0
        
        # 频率特性评估
        if 'frequency_range' in target_specs:
            freq_score = self._evaluate_frequency(waveform, target_specs['frequency_range'])
            score += freq_score
        
        # 幅度特性评估
        if 'amplitude_range' in target_specs:
            amp_score = self._evaluate_amplitude(waveform, target_specs['amplitude_range'])
            score += amp_score
        
        # 平滑度评估
        if 'smoothness' in target_specs:
            smooth_score = self._evaluate_smoothness(waveform)
            score += smooth_score
            
        return score
    
    def _evaluate_frequency(self, waveform: np.ndarray, 
                           freq_range: tuple) -> float:
        """评估频率特性"""
        fft = np.fft.fft(waveform)
        freqs = np.fft.fftfreq(len(waveform))
        dominant_freq = np.abs(freqs[np.argmax(np.abs(fft))])
        
        if freq_range[0] <= dominant_freq <= freq_range[1]:
            return 1.0
        else:
            return max(0, 1 - abs(dominant_freq - np.mean(freq_range)) / np.mean(freq_range))
    
    def _evaluate_amplitude(self, waveform: np.ndarray, 
                           amp_range: tuple) -> float:
        """评估幅度特性"""
        max_amp = np.max(np.abs(waveform))
        
        if amp_range[0] <= max_amp <= amp_range[1]:
            return 1.0
        else:
            return max(0, 1 - abs(max_amp - np.mean(amp_range)) / np.mean(amp_range))
    
    def _evaluate_smoothness(self, waveform: np.ndarray) -> float:
        """评估平滑度"""
        gradient = np.gradient(waveform)
        smoothness = 1 / (1 + np.std(gradient))
        return smoothness

# ==================== 模型管理器 ====================
class ModelManager:
    """AI模型管理器"""
    
    def __init__(self):
        self.models = {}
        self.model_configs = {}
    
    def register_model(self, name: str, model, config: Dict = None):
        """注册模型"""
        self.models[name] = model
        self.model_configs[name] = config or {}
    
    def get_model(self, name: str):
        """获取模型"""
        return self.models.get(name)
    
    def list_models(self) -> List[str]:
        """列出所有模型"""
        return list(self.models.keys())
    
    def save_model(self, name: str, filepath: str):
        """保存模型"""
        if name in self.models:
            model = self.models[name]
            if hasattr(model, 'model'):
                model.model.save(filepath)
            elif hasattr(model, 'generator'):
                model.generator.save(f"{filepath}_generator")
                model.discriminator.save(f"{filepath}_discriminator")
    
    def load_model(self, name: str, filepath: str, model_type: str = 'lstm'):
        """加载模型"""
        if model_type == 'lstm':
            model = LSTMPredictor()
            model.model = keras.models.load_model(filepath)
            model.is_trained = True
            self.register_model(name, model)
        elif model_type == 'gan':
            model = WaveformGAN()
            model.generator = keras.models.load_model(f"{filepath}_generator")
            model.discriminator = keras.models.load_model(f"{filepath}_discriminator")
            self.register_model(name, model)
