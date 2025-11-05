"""
Unit tests for Quantum Navigation Map Server
"""

import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from servers.quantum_navigation_server import QuantumNavigationServer


class TestQuantumNavigationServer:
    """Test suite for Quantum Navigation Server"""
    
    @pytest.fixture
    def server(self):
        """Create server instance for testing"""
        return QuantumNavigationServer()
    
    def test_server_initialization(self, server):
        """Test that server initializes correctly"""
        assert server.server_name == "Quantum Navigation Map Server"
        assert server.version == "1.0.0"
        assert len(server.route_network) > 0
    
    def test_get_server_info(self, server):
        """Test server info returns correct structure"""
        info = server.get_server_info()
        assert "name" in info
        assert "tools" in info
        assert len(info["tools"]) == 3
    
    def test_calculate_quantum_routes_success(self, server):
        """Test successful route calculation"""
        result = server.calculate_quantum_routes("New York", "Boston", mode="efficient")
        
        assert result["success"] is True
        assert result["origin"] == "New York"
        assert result["destination"] == "Boston"
        assert "routes" in result
        assert len(result["routes"]) > 0
        
        # Check route structure
        for route in result["routes"]:
            assert "route_name" in route
            assert "distance_km" in route
            assert "estimated_time_min" in route
            assert "confidence_score" in route
            assert "time_range" in route
            
            # Time range should be logical
            time_range = route["time_range"]
            assert time_range["optimistic"] <= time_range["expected"]
            assert time_range["expected"] <= time_range["pessimistic"]
    
    def test_calculate_quantum_routes_not_found(self, server):
        """Test route calculation with non-existent route"""
        result = server.calculate_quantum_routes("Mars", "Venus")
        
        assert result["success"] is False
        assert "error" in result
        assert "available_routes" in result
    
    def test_calculate_quantum_routes_modes(self, server):
        """Test different routing modes"""
        modes = ["fastest", "scenic", "safest", "adventurous", "efficient"]
        
        for mode in modes:
            result = server.calculate_quantum_routes("San Francisco", "Los Angeles", mode=mode)
            assert result["success"] is True
            assert result["routing_mode"] == mode
            
            # Routes should be sorted by suitability
            scores = [r["suitability_score"] for r in result["routes"]]
            assert scores == sorted(scores, reverse=True)
    
    def test_calculate_quantum_routes_risk_tolerance(self, server):
        """Test risk tolerance parameter"""
        result_low = server.calculate_quantum_routes(
            "New York", "Boston", mode="efficient", risk_tolerance=0.2
        )
        result_high = server.calculate_quantum_routes(
            "New York", "Boston", mode="efficient", risk_tolerance=0.8
        )
        
        assert result_low["success"] is True
        assert result_high["success"] is True
        assert result_low["risk_tolerance"] == 0.2
        assert result_high["risk_tolerance"] == 0.8
    
    def test_evaluate_route_confidence_success(self, server):
        """Test route confidence evaluation"""
        result = server.evaluate_route_confidence("New York", "Boston", "I-95 Express")
        
        assert result["success"] is True
        assert "route" in result
        assert "overall_confidence" in result
        assert "success_probability" in result
        assert "risk_assessment" in result
        assert "timing_reliability" in result
        
        # Check risk assessment
        risk = result["risk_assessment"]
        assert "level" in risk
        assert "factors" in risk
        assert "mitigation_strategies" in risk
        assert len(risk["mitigation_strategies"]) > 0
    
    def test_evaluate_route_confidence_invalid_route(self, server):
        """Test confidence evaluation with invalid route name"""
        result = server.evaluate_route_confidence("New York", "Boston", "Imaginary Highway")
        
        assert result["success"] is False
        assert "available_routes" in result
    
    def test_adaptive_reroute_success(self, server):
        """Test adaptive rerouting"""
        result = server.adaptive_reroute(
            "New York", "Boston", 
            conditions=["heavy traffic", "construction"]
        )
        
        assert result["success"] is True
        assert "current_conditions" in result
        assert "adapted_routes" in result
        assert "best_option" in result
        
        # Check that confidence was adjusted
        for route in result["adapted_routes"]:
            assert "original_confidence" in route
            assert "adjusted_confidence" in route
            assert "confidence_change" in route
            assert "condition_impact" in route
    
    def test_adaptive_reroute_no_conditions(self, server):
        """Test adaptive rerouting with no conditions"""
        result = server.adaptive_reroute("New York", "Boston", conditions=[])
        
        assert result["success"] is True
        # With no conditions, confidence should be mostly unchanged
        for route in result["adapted_routes"]:
            assert abs(route["confidence_change"]) < 0.1
    
    def test_adaptive_reroute_multiple_conditions(self, server):
        """Test with multiple adverse conditions"""
        result = server.adaptive_reroute(
            "San Francisco", "Los Angeles",
            conditions=["heavy traffic", "rain", "fog", "construction"]
        )
        
        assert result["success"] is True
        assert result["condition_severity"] in ["LOW", "MODERATE", "HIGH"]
        
        # Should show significant confidence changes
        changes = [abs(r["confidence_change"]) for r in result["adapted_routes"]]
        assert max(changes) > 0  # At least some change
    
    def test_quantum_state_generation(self, server):
        """Test quantum state representation"""
        result = server.calculate_quantum_routes("London", "Edinburgh")
        
        assert result["success"] is True
        for route in result["routes"]:
            assert "quantum_state" in route
            assert "|" in route["quantum_state"]  # Should use quantum notation
            assert "⟩" in route["quantum_state"]
    
    def test_bidirectional_routes(self, server):
        """Test that routes work in both directions"""
        result1 = server.calculate_quantum_routes("New York", "Boston")
        result2 = server.calculate_quantum_routes("Boston", "New York")
        
        assert result1["success"] is True
        assert result2["success"] is True
        # Should find the same route network
        assert len(result1["routes"]) == len(result2["routes"])


class TestQuantumNavigationEdgeCases:
    """Test edge cases and error handling"""
    
    @pytest.fixture
    def server(self):
        return QuantumNavigationServer()
    
    def test_same_origin_destination(self, server):
        """Test with same origin and destination"""
        result = server.calculate_quantum_routes("New York", "New York")
        # Should handle gracefully
        assert "success" in result
    
    def test_case_insensitive_locations(self, server):
        """Test case insensitive location matching"""
        result1 = server.calculate_quantum_routes("new york", "boston")
        result2 = server.calculate_quantum_routes("NEW YORK", "BOSTON")
        
        # At least one should succeed
        assert result1["success"] is True or result2["success"] is True
    
    def test_risk_tolerance_boundaries(self, server):
        """Test risk tolerance boundary values"""
        result_min = server.calculate_quantum_routes(
            "New York", "Boston", risk_tolerance=0.0
        )
        result_max = server.calculate_quantum_routes(
            "New York", "Boston", risk_tolerance=1.0
        )
        
        assert result_min["success"] is True
        assert result_max["success"] is True
    
    def test_confidence_scores_valid_range(self, server):
        """Test that all confidence scores are in valid range"""
        result = server.calculate_quantum_routes("San Francisco", "Los Angeles")
        
        assert result["success"] is True
        for route in result["routes"]:
            # Confidence scores should be between 0 and 100 (as percentage)
            assert 0 <= route["confidence_score"] <= 100
    
    def test_timing_estimates_positive(self, server):
        """Test that timing estimates are positive"""
        result = server.calculate_quantum_routes("London", "Edinburgh")
        
        assert result["success"] is True
        for route in result["routes"]:
            assert route["distance_km"] > 0
            assert route["estimated_time_min"] > 0
            assert route["time_range"]["optimistic"] > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
