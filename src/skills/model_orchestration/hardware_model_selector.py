#!/usr/bin/env python3
"""
Skill: hardware-model-selector
Domain: model_orchestration
Description: Provides a standardized framework for hardware-aware model routing by mapping system-level hardware characteristics to model requirements.
"""

import asyncio
import json
import logging
import subprocess
import time
from typing import Dict, Any, List, Optional, NamedTuple
from dataclasses import dataclass
from enum import Enum
import psutil

logger = logging.getLogger(__name__)

class QuantizationType(Enum):
    """Supported quantization types"""
    FP16 = "fp16"
    FP8 = "fp8"
    Q4 = "q4"
    AWQ = "awq"
    INT8 = "int8"

class HardwareType(Enum):
    """Hardware categories"""
    LAPTOP = "laptop"
    DESKTOP = "desktop"
    SERVER = "server"
    CLOUD = "cloud"
    UNKNOWN = "unknown"

@dataclass
class HardwareStats:
    """Hardware statistics for a device"""
    vram_total_gb: float
    vram_used_gb: float
    vram_available_gb: float
    compute_capability: Optional[str] = None
    cpu_cores: int = 0
    cpu_ram_gb: float = 0.0
    gpu_name: Optional[str] = None
    hardware_type: HardwareType = HardwareType.UNKNOWN

@dataclass
class ModelProfile:
    """Model configuration profile"""
    model_id: str
    quantization: QuantizationType
    vram_required_gb: float
    kv_cache_headroom_gb: float
    description: str

@dataclass
class SelectionResult:
    """Result of hardware model selection"""
    selected_model: str
    quantization: str
    execution_strategy: str
    vram_usage_gb: float
    headroom_gb: float
    reasoning: str
    fallback_model: Optional[str] = None

class HardwareModelSelector:
    """Hardware-aware model selection framework"""
    
    def __init__(self, min_headroom_gb: float = 2.0, preferred_quantization: str = "awq"):
        """
        Initialize the hardware model selector
        
        Args:
            min_headroom_gb: Minimum VRAM headroom in GB
            preferred_quantization: Preferred quantization type
        """
        self.min_headroom_gb = min_headroom_gb
        self.preferred_quantization = preferred_quantization
        
        # Pre-calculated VRAM requirements for common models
        self.model_profiles = self._initialize_model_profiles()
        
        # Hardware profile cache
        self._hardware_cache: Optional[HardwareStats] = None
        self._cache_timestamp = 0
        self._cache_ttl = 300  # 5 minutes
    
    def _initialize_model_profiles(self) -> List[ModelProfile]:
        """Initialize model profiles with VRAM requirements"""
        return [
            # Small models (for laptops and low-end devices)
            ModelProfile("Llama-3-8B-Q4", QuantizationType.Q4, 6.0, 2.0, "8B model with Q4 quantization"),
            ModelProfile("Llama-3-8B-AWQ", QuantizationType.AWQ, 7.0, 2.0, "8B model with AWQ quantization"),
            ModelProfile("Phi-3-mini-4K", QuantizationType.Q4, 4.0, 1.5, "4K context Phi-3 mini model"),
            
            # Medium models (for desktop and mid-range GPUs)
            ModelProfile("Llama-3-13B-Q4", QuantizationType.Q4, 10.0, 2.5, "13B model with Q4 quantization"),
            ModelProfile("Llama-3-13B-AWQ", QuantizationType.AWQ, 12.0, 2.5, "13B model with AWQ quantization"),
            ModelProfile("Mistral-7B", QuantizationType.Q4, 8.0, 2.0, "7B Mistral model"),
            
            # Large models (for high-end GPUs and servers)
            ModelProfile("Llama-3.1-70B-Q4", QuantizationType.Q4, 40.0, 5.0, "70B model with Q4 quantization"),
            ModelProfile("Llama-3.1-70B-AWQ", QuantizationType.AWQ, 45.0, 5.0, "70B model with AWQ quantization"),
            ModelProfile("Llama-3.1-70B-FP16", QuantizationType.FP16, 140.0, 10.0, "70B model with FP16"),
            
            # Very large models (for A100 clusters and datacenters)
            ModelProfile("Llama-3.1-405B-FP8", QuantizationType.FP8, 800.0, 50.0, "405B model with FP8 quantization"),
            ModelProfile("Llama-3.1-405B-FP16", QuantizationType.FP16, 1600.0, 100.0, "405B model with FP16"),
        ]
    
    async def get_hardware_stats(self) -> HardwareStats:
        """
        Get current hardware statistics with caching
        
        Returns:
            HardwareStats object with current system information
        """
        current_time = time.time()
        
        # Check cache
        if self._hardware_cache and (current_time - self._cache_timestamp) < self._cache_ttl:
            return self._hardware_cache
        
        try:
            # Get GPU stats using nvidia-smi if available
            gpu_stats = await self._get_gpu_stats()
            
            # Get CPU stats
            cpu_stats = self._get_cpu_stats()
            
            # Determine hardware type
            hardware_type = self._classify_hardware(gpu_stats, cpu_stats)
            
            stats = HardwareStats(
                vram_total_gb=gpu_stats.get('total', 0.0),
                vram_used_gb=gpu_stats.get('used', 0.0),
                vram_available_gb=gpu_stats.get('available', 0.0),
                compute_capability=gpu_stats.get('compute_capability'),
                cpu_cores=cpu_stats['cores'],
                cpu_ram_gb=cpu_stats['ram_gb'],
                gpu_name=gpu_stats.get('name'),
                hardware_type=hardware_type
            )
            
            # Cache the result
            self._hardware_cache = stats
            self._cache_timestamp = current_time
            
            logger.info(f"Hardware stats: {stats}")
            return stats
            
        except Exception as e:
            logger.error(f"Failed to get hardware stats: {e}")
            # Return fallback stats
            return HardwareStats(
                vram_total_gb=0.0,
                vram_used_gb=0.0,
                vram_available_gb=0.0,
                cpu_cores=psutil.cpu_count(),
                cpu_ram_gb=psutil.virtual_memory().total / (1024**3),
                hardware_type=HardwareType.UNKNOWN
            )
    
    async def _get_gpu_stats(self) -> Dict[str, Any]:
        """Get GPU statistics using nvidia-smi"""
        try:
            # Try to run nvidia-smi
            result = subprocess.run(
                ['nvidia-smi', '--query-gpu=memory.total,memory.used,memory.free,name,compute_cap', 
                 '--format=csv,noheader,nounits'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                if lines and lines[0]:
                    # Parse the first GPU (assuming single GPU for simplicity)
                    parts = lines[0].split(', ')
                    if len(parts) >= 5:
                        return {
                            'total': float(parts[0]) / 1024.0,  # Convert MB to GB
                            'used': float(parts[1]) / 1024.0,
                            'available': float(parts[2]) / 1024.0,
                            'name': parts[3],
                            'compute_capability': parts[4]
                        }
            
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError) as e:
            logger.warning(f"nvidia-smi not available or failed: {e}")
        
        # Fallback: try to detect if we have any GPU
        try:
            import torch
            if torch.cuda.is_available():
                return {
                    'total': torch.cuda.get_device_properties(0).total_memory / (1024**3),
                    'used': 0.0,  # Can't easily get this without nvidia-smi
                    'available': torch.cuda.get_device_properties(0).total_memory / (1024**3),
                    'name': torch.cuda.get_device_name(0),
                    'compute_capability': f"{torch.cuda.get_device_properties(0).major}.{torch.cuda.get_device_properties(0).minor}"
                }
        except ImportError:
            pass
        
        return {'total': 0.0, 'used': 0.0, 'available': 0.0, 'name': None, 'compute_capability': None}
    
    def _get_cpu_stats(self) -> Dict[str, Any]:
        """Get CPU statistics"""
        return {
            'cores': psutil.cpu_count(logical=False),
            'ram_gb': psutil.virtual_memory().total / (1024**3)
        }
    
    def _classify_hardware(self, gpu_stats: Dict[str, Any], cpu_stats: Dict[str, Any]) -> HardwareType:
        """Classify hardware type based on specs"""
        vram_gb = gpu_stats.get('total', 0.0)
        cores = cpu_stats['cores']
        
        if vram_gb == 0:
            return HardwareType.LAPTOP  # CPU-only, likely laptop
        
        if vram_gb <= 8:
            return HardwareType.LAPTOP
        elif vram_gb <= 24:
            return HardwareType.DESKTOP
        elif vram_gb <= 80:
            return HardwareType.SERVER
        else:
            return HardwareType.CLOUD
    
    def select_model(self, hardware_stats: HardwareStats) -> SelectionResult:
        """
        Select the optimal model for the given hardware
        
        Args:
            hardware_stats: Current hardware statistics
            
        Returns:
            SelectionResult with recommended model and configuration
        """
        available_vram = hardware_stats.vram_available_gb
        
        # Ensure we don't exceed 90% of total VRAM
        max_vram_usage = hardware_stats.vram_total_gb * 0.9
        
        # Filter models that fit within VRAM constraints
        viable_models = []
        for profile in self.model_profiles:
            if (profile.vram_required_gb + self.min_headroom_gb <= available_vram and
                profile.vram_required_gb <= max_vram_usage):
                viable_models.append(profile)
        
        if not viable_models:
            # No models fit, return fallback
            return SelectionResult(
                selected_model="Phi-3-mini-4K",
                quantization="q4",
                execution_strategy="cpu_fallback",
                vram_usage_gb=0.0,
                headroom_gb=0.0,
                fallback_model=None,
                reasoning=f"No GPU models fit in {available_vram:.1f}GB VRAM, using CPU fallback"
            )
        
        # Sort by preference: preferred quantization first, then smallest model
        viable_models.sort(key=lambda x: (
            0 if x.quantization.value == self.preferred_quantization else 1,
            x.vram_required_gb
        ))
        
        best_model = viable_models[0]
        
        # Determine execution strategy
        if hardware_stats.hardware_type in [HardwareType.SERVER, HardwareType.CLOUD]:
            strategy = "gpu_optimal"
        elif hardware_stats.hardware_type == HardwareType.DESKTOP:
            strategy = "gpu_balanced"
        else:
            strategy = "gpu_conservative"
        
        # Find fallback model (smaller than current)
        fallback_model = None
        for profile in viable_models:
            if profile.vram_required_gb < best_model.vram_required_gb:
                fallback_model = profile.model_id
                break
        
        return SelectionResult(
            selected_model=best_model.model_id,
            quantization=best_model.quantization.value,
            execution_strategy=strategy,
            vram_usage_gb=best_model.vram_required_gb,
            headroom_gb=available_vram - best_model.vram_required_gb,
            fallback_model=fallback_model,
            reasoning=f"Selected {best_model.model_id} for {hardware_stats.hardware_type.value} with {available_vram:.1f}GB available VRAM"
        )
    
    async def invoke_selection(self, input_data: Dict[str, Any]) -> SelectionResult:
        """
        Main selection method that can be called externally
        
        Args:
            input_data: Input data (can contain hardware_stats or device description)
            
        Returns:
            SelectionResult
        """
        # If hardware stats are provided directly, use them
        if 'hardware_stats' in input_data:
            hardware_stats = HardwareStats(**input_data['hardware_stats'])
        else:
            # Get current hardware stats
            hardware_stats = await self.get_hardware_stats()
        
        # Perform selection
        result = self.select_model(hardware_stats)
        
        logger.info(f"Model selection result: {result}")
        return result

# Global selector instance
_selector = HardwareModelSelector()

async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Entry point for skill invocation.
    
    Args:
        payload: dict of input parameters including:
            - action: "select", "get_hardware", "list_models"
            - hardware_stats: optional hardware statistics
            - min_headroom_gb: optional override for headroom
            - preferred_quantization: optional override for quantization
            
    Returns:
        dict with 'result' key and optional 'metadata'
    """
    action = payload.get("action", "select")
    
    try:
        if action == "select":
            # Override defaults if provided
            if 'min_headroom_gb' in payload:
                _selector.min_headroom_gb = payload['min_headroom_gb']
            if 'preferred_quantization' in payload:
                _selector.preferred_quantization = payload['preferred_quantization']
            
            result = await _selector.invoke_selection(payload)
            
            return {
                "result": {
                    "selected_model": result.selected_model,
                    "quantization": result.quantization,
                    "execution_strategy": result.execution_strategy,
                    "vram_usage_gb": result.vram_usage_gb,
                    "headroom_gb": result.headroom_gb,
                    "fallback_model": result.fallback_model,
                    "reasoning": result.reasoning
                },
                "metadata": {
                    "action": "select",
                    "timestamp": time.time(),
                    "hardware_type": _selector._hardware_cache.hardware_type.value if _selector._hardware_cache else "unknown"
                }
            }
        
        elif action == "get_hardware":
            stats = await _selector.get_hardware_stats()
            
            return {
                "result": {
                    "vram_total_gb": stats.vram_total_gb,
                    "vram_used_gb": stats.vram_used_gb,
                    "vram_available_gb": stats.vram_available_gb,
                    "compute_capability": stats.compute_capability,
                    "cpu_cores": stats.cpu_cores,
                    "cpu_ram_gb": stats.cpu_ram_gb,
                    "gpu_name": stats.gpu_name,
                    "hardware_type": stats.hardware_type.value
                },
                "metadata": {
                    "action": "get_hardware",
                    "timestamp": time.time()
                }
            }
        
        elif action == "list_models":
            models = []
            for profile in _selector.model_profiles:
                models.append({
                    "model_id": profile.model_id,
                    "quantization": profile.quantization.value,
                    "vram_required_gb": profile.vram_required_gb,
                    "kv_cache_headroom_gb": profile.kv_cache_headroom_gb,
                    "description": profile.description
                })
            
            return {
                "result": models,
                "metadata": {
                    "action": "list_models",
                    "total_models": len(models),
                    "timestamp": time.time()
                }
            }
        
        else:
            return {
                "result": {
                    "error": f"Unknown action: {action}"
                },
                "metadata": {
                    "action": action,
                    "timestamp": time.time()
                }
            }
    
    except Exception as e:
        logger.error(f"Error in hardware_model_selector: {e}")
        return {
            "result": {
                "error": str(e)
            },
            "metadata": {
                "action": action,
                "timestamp": time.time()
            }
        }

# Example usage function
async def example_usage():
    """Example of how to use the hardware model selector skill"""
    
    # Get hardware stats
    result = await invoke({"action": "get_hardware"})
    print(f"Hardware stats: {result}")
    
    # Select model
    selection = await invoke({"action": "select"})
    print(f"Model selection: {selection}")
    
    # List available models
    models = await invoke({"action": "list_models"})
    print(f"Available models: {len(models['result'])}")

if __name__ == "__main__":
    asyncio.run(example_usage())