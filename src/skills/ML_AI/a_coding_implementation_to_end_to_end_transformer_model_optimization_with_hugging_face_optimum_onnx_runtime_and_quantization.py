#!/usr/bin/env python3
"""
A Coding Implementation to End-to-End Transformer Model Optimization with Hugging Face Optimum, ONNX Runtime, and Quantization

This skill provides comprehensive implementation patterns for optimizing transformer models
using Hugging Face Optimum, ONNX Runtime, and quantization techniques. It covers the
complete workflow from model loading to deployment optimization.

Source: A Coding Implementation to End-to-End Transformer Model Optimization with Hugging Face Optimum, ONNX Runtime, and Quantization.ipynb
Type: Jupyter Notebook tutorial
Category: ML Project Codes
"""

import os
import json
import logging
import subprocess
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path
import tempfile

# Core dependencies for transformer model optimization
try:
    import torch
    import transformers
    import onnxruntime
    import numpy as np
    from transformers import (
        AutoTokenizer, 
        AutoModelForSequenceClassification,
        pipeline
    )
    from optimum.onnxruntime import (
        ORTModelForSequenceClassification,
        ORTOptimizer,
        ORTQuantizer
    )
    from optimum.onnxruntime.configuration import OptimizationConfig
    from onnxruntime.quantization import QuantizationMode
except ImportError as e:
    raise ImportError(f"Required dependencies not installed: {e}")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TransformerModelOptimizer:
    """
    A comprehensive class for optimizing transformer models using Hugging Face Optimum,
    ONNX Runtime, and quantization techniques.
    """
    
    def __init__(self, model_name: str = "distilbert-base-uncased-finetuned-sst-2-english"):
        """
        Initialize the optimizer with a pre-trained model.
        
        Args:
            model_name (str): Name of the Hugging Face model to optimize
        """
        self.model_name = model_name
        self.tokenizer = None
        self.original_model = None
        self.onnx_model = None
        self.quantized_model = None
        self.optimization_config = None
        self.quantization_config = None
        
        logger.info(f"Initializing optimizer for model: {model_name}")
    
    def setup_environment(self) -> bool:
        """
        Set up the environment and load the base model.
        
        Returns:
            bool: True if setup successful, False otherwise
        """
        try:
            # Load tokenizer and model
            logger.info("Loading tokenizer and model...")
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.original_model = AutoModelForSequenceClassification.from_pretrained(
                self.model_name
            )
            
            logger.info("Environment setup complete")
            return True
            
        except Exception as e:
            logger.error(f"Failed to setup environment: {e}")
            return False
    
    def create_optimization_config(self, optimization_level: int = 99) -> OptimizationConfig:
        """
        Create optimization configuration for ONNX model.
        
        Args:
            optimization_level (int): Optimization level (0-99)
            
        Returns:
            OptimizationConfig: Configuration for model optimization
        """
        self.optimization_config = OptimizationConfig(
            optimization_level=optimization_level,
            optimize_for_gpu=torch.cuda.is_available(),
            fp16=True if torch.cuda.is_available() else False
        )
        
        logger.info(f"Created optimization config: level={optimization_level}")
        return self.optimization_config
    
    def convert_to_onnx(self, output_dir: str = "./onnx_models") -> bool:
        """
        Convert PyTorch model to ONNX format.
        
        Args:
            output_dir (str): Directory to save ONNX model
            
        Returns:
            bool: True if conversion successful, False otherwise
        """
        try:
            Path(output_dir).mkdir(parents=True, exist_ok=True)
            
            logger.info("Converting model to ONNX format...")
            
            # Create ONNX model
            self.onnx_model = ORTModelForSequenceClassification.from_pretrained(
                self.model_name,
                from_transformers=True,
                export=True,
                output_dir=output_dir
            )
            
            logger.info(f"ONNX model saved to: {output_dir}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to convert to ONNX: {e}")
            return False
    
    def optimize_onnx_model(self, onnx_path: str, output_path: str) -> bool:
        """
        Optimize ONNX model using ORT Optimizer.
        
        Args:
            onnx_path (str): Path to input ONNX model
            output_path (str): Path to save optimized model
            
        Returns:
            bool: True if optimization successful, False otherwise
        """
        try:
            if not self.optimization_config:
                self.create_optimization_config()
            
            logger.info("Optimizing ONNX model...")
            
            # Create optimizer
            optimizer = ORTOptimizer.from_pretrained(onnx_path)
            
            # Apply optimization
            optimizer.optimize(
                save_dir=output_path,
                optimization_config=self.optimization_config
            )
            
            logger.info(f"Optimized model saved to: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to optimize ONNX model: {e}")
            return False
    
    def create_quantization_config(self, quantization_mode: str = "dynamic") -> Any:
        """
        Create quantization configuration.
        
        Args:
            quantization_mode (str): Quantization mode ("dynamic", "static", "qat")
            
        Returns:
            Any: Quantization configuration
        """
        if quantization_mode == "dynamic":
            self.quantization_config = {
                "is_static": False,
                "weight_type": QuantizationMode.INT8,
                "per_channel": True
            }
        elif quantization_mode == "static":
            self.quantization_config = {
                "is_static": True,
                "weight_type": QuantizationMode.INT8,
                "per_channel": True
            }
        else:
            raise ValueError(f"Unsupported quantization mode: {quantization_mode}")
        
        logger.info(f"Created quantization config: {quantization_mode}")
        return self.quantization_config
    
    def quantize_model(self, onnx_path: str, output_path: str, 
                      quantization_mode: str = "dynamic") -> bool:
        """
        Quantize ONNX model to reduce size and improve inference speed.
        
        Args:
            onnx_path (str): Path to ONNX model to quantize
            output_path (str): Path to save quantized model
            quantization_mode (str): Type of quantization to apply
            
        Returns:
            bool: True if quantization successful, False otherwise
        """
        try:
            if not self.quantization_config:
                self.create_quantization_config(quantization_mode)
            
            logger.info(f"Quantizing model with mode: {quantization_mode}")
            
            # Create quantizer
            quantizer = ORTQuantizer.from_pretrained(onnx_path)
            
            # Apply quantization
            quantizer.quantize(
                save_dir=output_path,
                quantization_config=self.quantization_config
            )
            
            logger.info(f"Quantized model saved to: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to quantize model: {e}")
            return False
    
    def benchmark_models(self, test_texts: List[str]) -> Dict[str, Dict[str, float]]:
        """
        Benchmark original, ONNX, and quantized models.
        
        Args:
            test_texts (List[str]): List of texts to test inference on
            
        Returns:
            Dict[str, Dict[str, float]]: Benchmark results for each model
        """
        results = {}
        
        # Test original PyTorch model
        if self.original_model and self.tokenizer:
            results["pytorch"] = self._benchmark_pytorch_model(test_texts)
        
        # Test ONNX model
        if self.onnx_model:
            results["onnx"] = self._benchmark_onnx_model(test_texts)
        
        # Test quantized model
        if self.quantized_model:
            results["quantized"] = self._benchmark_quantized_model(test_texts)
        
        return results
    
    def _benchmark_pytorch_model(self, test_texts: List[str]) -> Dict[str, float]:
        """Benchmark PyTorch model."""
        import time
        
        self.original_model.eval()
        
        # Warmup
        for _ in range(3):
            inputs = self.tokenizer("warmup", return_tensors="pt")
            with torch.no_grad():
                _ = self.original_model(**inputs)
        
        # Benchmark
        times = []
        for text in test_texts:
            inputs = self.tokenizer(text, return_tensors="pt")
            
            start_time = time.perf_counter()
            with torch.no_grad():
                outputs = self.original_model(**inputs)
            end_time = time.perf_counter()
            
            times.append((end_time - start_time) * 1000)  # Convert to ms
        
        return {
            "avg_latency_ms": np.mean(times),
            "min_latency_ms": np.min(times),
            "max_latency_ms": np.max(times),
            "std_latency_ms": np.std(times)
        }
    
    def _benchmark_onnx_model(self, test_texts: List[str]) -> Dict[str, float]:
        """Benchmark ONNX model."""
        import time
        
        # Create ONNX inference session
        session = onnxruntime.InferenceSession(
            self.onnx_model.model_path,
            providers=['CUDAExecutionProvider'] if torch.cuda.is_available() else ['CPUExecutionProvider']
        )
        
        # Warmup
        for _ in range(3):
            inputs = self.tokenizer("warmup", return_tensors="np")
            _ = session.run(None, inputs.data)
        
        # Benchmark
        times = []
        for text in test_texts:
            inputs = self.tokenizer(text, return_tensors="np")
            
            start_time = time.perf_counter()
            outputs = session.run(None, inputs.data)
            end_time = time.perf_counter()
            
            times.append((end_time - start_time) * 1000)  # Convert to ms
        
        return {
            "avg_latency_ms": np.mean(times),
            "min_latency_ms": np.min(times),
            "max_latency_ms": np.max(times),
            "std_latency_ms": np.std(times)
        }
    
    def _benchmark_quantized_model(self, test_texts: List[str]) -> Dict[str, float]:
        """Benchmark quantized model."""
        import time
        
        # Create quantized ONNX inference session
        session = onnxruntime.InferenceSession(
            self.quantized_model.model_path,
            providers=['CUDAExecutionProvider'] if torch.cuda.is_available() else ['CPUExecutionProvider']
        )
        
        # Warmup
        for _ in range(3):
            inputs = self.tokenizer("warmup", return_tensors="np")
            _ = session.run(None, inputs.data)
        
        # Benchmark
        times = []
        for text in test_texts:
            inputs = self.tokenizer(text, return_tensors="np")
            
            start_time = time.perf_counter()
            outputs = session.run(None, inputs.data)
            end_time = time.perf_counter()
            
            times.append((end_time - start_time) * 1000)  # Convert to ms
        
        return {
            "avg_latency_ms": np.mean(times),
            "min_latency_ms": np.min(times),
            "max_latency_ms": np.max(times),
            "std_latency_ms": np.std(times)
        }
    
    def get_model_size(self, model_path: str) -> float:
        """
        Get model file size in MB.
        
        Args:
            model_path (str): Path to model file
            
        Returns:
            float: Model size in MB
        """
        if os.path.exists(model_path):
            size_bytes = os.path.getsize(model_path)
            return size_bytes / (1024 * 1024)  # Convert to MB
        return 0.0
    
    def create_deployment_package(self, output_dir: str = "./deployment_package") -> bool:
        """
        Create a deployment package with optimized models.
        
        Args:
            output_dir (str): Directory to save deployment package
            
        Returns:
            bool: True if package creation successful, False otherwise
        """
        try:
            Path(output_dir).mkdir(parents=True, exist_ok=True)
            
            # Copy optimized models
            if self.onnx_model:
                import shutil
                shutil.copytree(
                    os.path.dirname(self.onnx_model.model_path),
                    os.path.join(output_dir, "onnx_model"),
                    dirs_exist_ok=True
                )
            
            if self.quantized_model:
                import shutil
                shutil.copytree(
                    os.path.dirname(self.quantized_model.model_path),
                    os.path.join(output_dir, "quantized_model"),
                    dirs_exist_ok=True
                )
            
            # Create deployment configuration
            config = {
                "model_name": self.model_name,
                "optimization_level": self.optimization_config.optimization_level if self.optimization_config else None,
                "quantization_mode": self.quantization_config.get("is_static", False) if self.quantization_config else None,
                "recommended_provider": "CUDAExecutionProvider" if torch.cuda.is_available() else "CPUExecutionProvider"
            }
            
            with open(os.path.join(output_dir, "deployment_config.json"), "w") as f:
                json.dump(config, f, indent=2)
            
            logger.info(f"Deployment package created at: {output_dir}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to create deployment package: {e}")
            return False


def optimize_transformer_model(
    model_name: str = "distilbert-base-uncased-finetuned-sst-2-english",
    output_dir: str = "./optimized_models",
    optimization_level: int = 99,
    quantization_mode: str = "dynamic"
) -> Dict[str, Any]:
    """
    Main function to optimize a transformer model end-to-end.
    
    Args:
        model_name (str): Name of the Hugging Face model to optimize
        output_dir (str): Directory to save optimized models
        optimization_level (int): ONNX optimization level (0-99)
        quantization_mode (str): Quantization mode ("dynamic", "static", "qat")
        
    Returns:
        Dict[str, Any]: Results of the optimization process
    """
    optimizer = TransformerModelOptimizer(model_name)
    
    # Setup environment
    if not optimizer.setup_environment():
        return {"success": False, "error": "Failed to setup environment"}
    
    # Create optimization config
    optimizer.create_optimization_config(optimization_level)
    
    # Convert to ONNX
    onnx_dir = os.path.join(output_dir, "onnx_model")
    if not optimizer.convert_to_onnx(onnx_dir):
        return {"success": False, "error": "Failed to convert to ONNX"}
    
    # Optimize ONNX model
    optimized_dir = os.path.join(output_dir, "optimized_model")
    onnx_path = os.path.join(onnx_dir, "model.onnx")
    if not optimizer.optimize_onnx_model(onnx_path, optimized_dir):
        return {"success": False, "error": "Failed to optimize ONNX model"}
    
    # Quantize model
    quantized_dir = os.path.join(output_dir, "quantized_model")
    optimized_path = os.path.join(optimized_dir, "model.onnx")
    if not optimizer.quantize_model(optimized_path, quantized_dir, quantization_mode):
        return {"success": False, "error": "Failed to quantize model"}
    
    # Benchmark models
    test_texts = [
        "This is a positive review",
        "This is a negative review", 
        "The movie was okay",
        "I love this product",
        "I hate this product"
    ]
    
    benchmark_results = optimizer.benchmark_models(test_texts)
    
    # Get model sizes
    sizes = {
        "original_onnx_mb": optimizer.get_model_size(onnx_path),
        "optimized_onnx_mb": optimizer.get_model_size(os.path.join(optimized_dir, "model.onnx")),
        "quantized_onnx_mb": optimizer.get_model_size(os.path.join(quantized_dir, "model.onnx"))
    }
    
    # Create deployment package
    deployment_dir = os.path.join(output_dir, "deployment_package")
    optimizer.create_deployment_package(deployment_dir)
    
    return {
        "success": True,
        "model_name": model_name,
        "optimization_level": optimization_level,
        "quantization_mode": quantization_mode,
        "benchmark_results": benchmark_results,
        "model_sizes_mb": sizes,
        "output_directory": output_dir,
        "deployment_package": deployment_dir
    }


def validate_optimization_results(results: Dict[str, Any]) -> bool:
    """
    Validate that optimization results meet expected criteria.
    
    Args:
        results (Dict[str, Any]): Results from optimize_transformer_model
        
    Returns:
        bool: True if validation passes, False otherwise
    """
    if not results.get("success"):
        logger.error("Optimization failed")
        return False
    
    benchmark = results.get("benchmark_results", {})
    
    # Check if we have results for all model types
    required_models = ["pytorch", "onnx", "quantized"]
    for model_type in required_models:
        if model_type not in benchmark:
            logger.error(f"Missing benchmark results for {model_type}")
            return False
    
    # Check if quantized model is faster than original
    pytorch_latency = benchmark["pytorch"]["avg_latency_ms"]
    quantized_latency = benchmark["quantized"]["avg_latency_ms"]
    
    if quantized_latency >= pytorch_latency:
        logger.warning(f"Quantized model ({quantized_latency:.2f}ms) not faster than PyTorch ({pytorch_latency:.2f}ms)")
    
    # Check if models are smaller
    sizes = results.get("model_sizes_mb", {})
    if sizes.get("quantized_onnx_mb", 0) >= sizes.get("original_onnx_mb", 0):
        logger.warning("Quantized model not smaller than original")
    
    logger.info("Optimization validation completed successfully")
    return True


def main():
    """Main execution function."""
    print("Transformer Model Optimization with Hugging Face Optimum, ONNX Runtime, and Quantization")
    print("=" * 80)
    
    # Example usage
    results = optimize_transformer_model(
        model_name="distilbert-base-uncased-finetuned-sst-2-english",
        output_dir="./optimized_models",
        optimization_level=99,
        quantization_mode="dynamic"
    )
    
    if results["success"]:
        print("\n✅ Optimization completed successfully!")
        print(f"Model: {results['model_name']}")
        print(f"Optimization Level: {results['optimization_level']}")
        print(f"Quantization Mode: {results['quantization_mode']}")
        
        print("\n📊 Benchmark Results:")
        for model_type, metrics in results["benchmark_results"].items():
            print(f"  {model_type.upper()}: {metrics['avg_latency_ms']:.2f}ms avg latency")
        
        print("\n📏 Model Sizes:")
        for model_type, size in results["model_sizes_mb"].items():
            print(f"  {model_type}: {size:.2f} MB")
        
        print(f"\n📁 Output Directory: {results['output_directory']}")
        print(f"📦 Deployment Package: {results['deployment_package']}")
        
        # Validate results
        if validate_optimization_results(results):
            print("\n✅ All validations passed!")
        else:
            print("\n⚠️  Some validations failed - check logs for details")
    
    else:
        print(f"\n❌ Optimization failed: {results.get('error')}")


if __name__ == "__main__":
    main()