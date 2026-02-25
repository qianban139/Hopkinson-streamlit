"""
控制系统模块
包含安全监控和中央控制系统
"""
import numpy as np
import threading
from queue import Queue
from datetime import datetime, timedelta
from typing import Dict, Tuple, List, Optional
from dataclasses import dataclass
from enum import Enum
import random
import math
import time

# ==================== 安全等级枚举 ====================
class SafetyLevel(Enum):
    """安全等级枚举"""
    NORMAL = "normal"
    WARNING = "warning"
    DANGER = "danger"
    CRITICAL = "critical"

# ==================== 安全阈值配置 ====================
@dataclass
class SafetyThresholds:
    """安全阈值数据类"""
    voltage: float = 1000.0          # 电压阈值 (V)
    current: float = 50.0            # 电流阈值 (A)
    temperature: float = 85.0        # 温度阈值 (°C)
    capacitor_charge: float = 0.9    # 电容充电阈值
    discharge_rate: float = 5.0      # 放电速率阈值
    insulation_resistance: float = 200.0  # 绝缘电阻阈值 (MΩ)
    ground_resistance: float = 1.0   # 接地电阻阈值 (Ω)

# ==================== 安全监控器 ====================
class SafetyMonitor:
    """高压安全监控器"""
    
    def __init__(self, thresholds: SafetyThresholds = None):
        """
        初始化安全监控器
        
        Args:
            thresholds: 安全阈值配置
        """
        self.thresholds = thresholds or SafetyThresholds()
        
        self.warning_levels = {
            SafetyLevel.NORMAL: "🟢 正常",
            SafetyLevel.WARNING: "🟡 警告",
            SafetyLevel.DANGER: "🔴 危险",
            SafetyLevel.CRITICAL: "⛔ 紧急"
        }
        
        self.safety_history: List[Dict] = []
        self.last_check_time = datetime.now()
        self.max_history_size = 1000
    
    def check_safety_status(self, sensor_data: Dict[str, float]) -> Tuple[SafetyLevel, str, Dict]:
        """
        检查安全状态
        
        Args:
            sensor_data: 传感器数据字典
            
        Returns:
            (安全等级, 状态描述, 详细数据)
        """
        warnings_list = []
        max_level = SafetyLevel.NORMAL
        
        # 电压检测
        if 'voltage' in sensor_data:
            voltage = sensor_data['voltage']
            if voltage > self.thresholds.voltage * 1.2:
                warnings_list.append(f"电压过高: {voltage:.1f}V > {self.thresholds.voltage*1.2:.1f}V")
                max_level = SafetyLevel.CRITICAL if voltage > self.thresholds.voltage * 1.3 else SafetyLevel.DANGER
            elif voltage > self.thresholds.voltage:
                warnings_list.append(f"电压警告: {voltage:.1f}V > {self.thresholds.voltage:.1f}V")
                max_level = SafetyLevel.WARNING if max_level != SafetyLevel.DANGER else max_level
        
        # 电流检测
        if 'current' in sensor_data:
            current = sensor_data['current']
            if current > self.thresholds.current * 1.2:
                warnings_list.append(f"电流过大: {current:.1f}A > {self.thresholds.current*1.2:.1f}A")
                max_level = SafetyLevel.CRITICAL if current > self.thresholds.current * 1.3 else SafetyLevel.DANGER
            elif current > self.thresholds.current:
                warnings_list.append(f"电流警告: {current:.1f}A > {self.thresholds.current:.1f}A")
                max_level = SafetyLevel.WARNING if max_level.value != 'danger' else max_level
        
        # 温度检测
        if 'temperature' in sensor_data:
            temp = sensor_data['temperature']
            if temp > self.thresholds.temperature * 1.1:
                warnings_list.append(f"温度过高: {temp:.1f}°C > {self.thresholds.temperature*1.1:.1f}°C")
                max_level = SafetyLevel.CRITICAL if temp > self.thresholds.temperature * 1.2 else SafetyLevel.DANGER
        
        # 电容状态检测
        if 'capacitor_charge' in sensor_data:
            charge = sensor_data['capacitor_charge']
            if charge > self.thresholds.capacitor_charge:
                warnings_list.append(f"电容充电过高: {charge:.2f} > {self.thresholds.capacitor_charge:.2f}")
                max_level = SafetyLevel.DANGER if max_level != SafetyLevel.CRITICAL else max_level
        
        # 绝缘电阻检测
        if 'insulation_resistance' in sensor_data:
            insulation = sensor_data['insulation_resistance']
            if insulation < self.thresholds.insulation_resistance:
                warnings_list.append(f"绝缘电阻过低: {insulation:.0f} MΩ")
                max_level = SafetyLevel.WARNING
        
        # 接地电阻检测
        if 'ground_resistance' in sensor_data:
            ground = sensor_data['ground_resistance']
            if ground > self.thresholds.ground_resistance:
                warnings_list.append(f"接地电阻过高: {ground:.2f} Ω")
                max_level = SafetyLevel.WARNING
        
        # 生成状态描述
        status_desc = self.warning_levels.get(max_level, '🟢 正常')
        if warnings_list:
            status_desc += f" - {', '.join(warnings_list[:2])}"
        
        # 记录安全历史
        safety_record = {
            'timestamp': datetime.now(),
            'level': max_level,
            'data': sensor_data.copy(),
            'warnings': warnings_list.copy()
        }
        self.safety_history.append(safety_record)
        
        # 保持历史记录在合理范围内
        if len(self.safety_history) > self.max_history_size:
            self.safety_history = self.safety_history[-self.max_history_size:]
        
        return max_level, status_desc, safety_record
    
    def get_safety_summary(self, hours: int = 24) -> Dict:
        """
        获取安全摘要
        
        Args:
            hours: 时间范围(小时)
            
        Returns:
            安全统计摘要
        """
        cutoff_time = datetime.now() - timedelta(hours=hours)
        recent_history = [r for r in self.safety_history if r['timestamp'] > cutoff_time]
        
        if not recent_history:
            return {
                'total': 0, 
                'normal': 0, 
                'warning': 0, 
                'danger': 0, 
                'critical': 0,
                'normal_percent': 0.0,
                'warning_percent': 0.0,
                'danger_percent': 0.0,
                'critical_percent': 0.0
            }
        
        summary = {
            'total': len(recent_history),
            'normal': len([r for r in recent_history if r['level'] == SafetyLevel.NORMAL]),
            'warning': len([r for r in recent_history if r['level'] == SafetyLevel.WARNING]),
            'danger': len([r for r in recent_history if r['level'] == SafetyLevel.DANGER]),
            'critical': len([r for r in recent_history if r['level'] == SafetyLevel.CRITICAL]),
        }
        
        # 计算百分比
        for level in ['normal', 'warning', 'danger', 'critical']:
            summary[f'{level}_percent'] = summary[level] / summary['total'] * 100 if summary['total'] > 0 else 0.0
        
        return summary
    
    def get_recent_alerts(self, count: int = 10) -> List[Dict]:
        """获取最近的警报"""
        alerts = [r for r in self.safety_history if r['level'] != SafetyLevel.NORMAL]
        return sorted(alerts, key=lambda x: x['timestamp'], reverse=True)[:count]

# ==================== 传感器模拟器 ====================
class SensorSimulator:
    """传感器数据模拟器"""
    
    def __init__(self, seed: int = None):
        """
        初始化模拟器
        
        Args:
            seed: 随机种子
        """
        if seed:
            random.seed(seed)
        self.time_factor = 0
    
    def generate_data(self) -> Dict[str, float]:
        """生成模拟传感器数据"""
        self.time_factor += 0.1
        time_val = math.sin(self.time_factor) * 0.3 + 0.7
        
        return {
            'voltage': 800 + random.uniform(-50, 50) + time_val * 200,
            'current': 30 + random.uniform(-5, 5),
            'temperature': 60 + random.uniform(-5, 5),
            'capacitor_charge': 0.7 + random.uniform(-0.1, 0.1),
            'discharge_rate': 3.0 + random.uniform(-1, 1),
            'insulation_resistance': 1000 + random.uniform(-100, 100),
            'ground_resistance': 0.1 + random.uniform(-0.05, 0.05),
        }
    
    def generate_waveform(self, length: int = 1000, 
                         frequency: float = 1.0,
                         amplitude: float = 1.0,
                         noise_level: float = 0.1) -> np.ndarray:
        """生成模拟波形"""
        t = np.linspace(0, 10, length)
        waveform = amplitude * np.sin(2 * np.pi * frequency * t)
        noise = noise_level * np.random.randn(length)
        return waveform + noise

# ==================== 中央控制系统 ====================
class CentralControlSystem:
    """中央控制系统"""
    
    def __init__(self):
        """初始化控制系统"""
        from utils.ai_models import LSTMPredictor, WaveformGAN
        
        self.lstm_predictor = LSTMPredictor()
        self.waveform_gan = WaveformGAN()
        self.control_parameters = {}
        self.real_time_data = Queue()
        self.is_running = False
        self.safety_monitor = SafetyMonitor()
        self.sensor_simulator = SensorSimulator()
        
        # 安全相关参数
        self.safety_enabled = True
        self.auto_shutdown_enabled = True
        self.emergency_shutdown_count = 0
        self.max_emergency_shutdowns = 3
        self.last_safety_check = datetime.now()
        
        # 系统状态
        self.system_status = "stopped"
        self.operation_mode = "simulation"
    
    def initialize_system(self, historical_data: np.ndarray):
        """初始化系统
        
        Args:
            historical_data: 历史数据
        """
        # 训练LSTM模型
        self.lstm_predictor.build_model((50, historical_data.shape[1] if len(historical_data.shape) > 1 else 1))
        self.lstm_predictor.train(historical_data, epochs=50, verbose=0)
        self.system_status = "initialized"
    
    def waveform_adaptive_control(self, current_waveform: np.ndarray, 
                                target_specifications: Dict) -> np.ndarray:
        """波形自适应调控
        
        Args:
            current_waveform: 当前波形
            target_specifications: 目标规格
            
        Returns:
            调控后的波形
        """
        # 使用LSTM预测未来趋势
        if len(current_waveform) >= 50:
            future_trend = self.lstm_predictor.predict(current_waveform[-50:])
        
        # 使用GAN生成满足规格的波形
        adapted_waveform = self.waveform_gan.adaptive_waveform_control(target_specifications)
        
        return adapted_waveform
    
    def perform_safety_check(self) -> Tuple[bool, str, Dict]:
        """执行安全检查
        
        Returns:
            (是否安全, 状态描述, 详细信息)
        """
        sensor_data = self.sensor_simulator.generate_data()
        level, description, record = self.safety_monitor.check_safety_status(sensor_data)
        
        self.last_safety_check = datetime.now()
        
        is_safe = True
        action = "无"
        
        if level == SafetyLevel.CRITICAL and self.auto_shutdown_enabled:
            is_safe = False
            action = "紧急停机"
            self.emergency_shutdown()
        elif level == SafetyLevel.DANGER and self.auto_shutdown_enabled:
            is_safe = False
            action = "安全停机"
            self.safe_shutdown()
        elif level == SafetyLevel.WARNING:
            action = "警告通知"
        
        return is_safe, description, {
            'action': action, 
            'data': sensor_data, 
            'level': level
        }
    
    def emergency_shutdown(self):
        """紧急停机"""
        self.is_running = False
        self.system_status = "emergency_stopped"
        self.emergency_shutdown_count += 1
        
        if self.emergency_shutdown_count >= self.max_emergency_shutdowns:
            self.safety_enabled = False
    
    def safe_shutdown(self):
        """安全停机"""
        self.is_running = False
        self.system_status = "stopped"
    
    def start_real_time_control(self):
        """启动实时控制系统"""
        self.is_running = True
        self.system_status = "running"
        control_thread = threading.Thread(target=self._real_time_control_loop)
        control_thread.daemon = True
        control_thread.start()
    
    def _real_time_control_loop(self):
        """实时控制循环"""
        while self.is_running:
            if not self.real_time_data.empty():
                current_data = self.real_time_data.get()
                
                # 执行实时控制逻辑
                controlled_waveform = self.waveform_adaptive_control(
                    current_data, self.control_parameters)
                
                # 发送控制指令到执行器
                self._send_control_signal(controlled_waveform)
            
            time.sleep(0.01)  # 10ms周期
    
    def _send_control_signal(self, control_signal: np.ndarray):
        """发送控制信号"""
        pass  # 实际实现中发送到硬件
    
    def get_system_status(self) -> Dict:
        """获取系统状态"""
        return {
            'status': self.system_status,
            'is_running': self.is_running,
            'safety_enabled': self.safety_enabled,
            'emergency_count': self.emergency_shutdown_count,
            'last_check': self.last_safety_check,
            'operation_mode': self.operation_mode
        }
    
    def set_control_parameters(self, params: Dict):
        """设置控制参数"""
        self.control_parameters.update(params)
