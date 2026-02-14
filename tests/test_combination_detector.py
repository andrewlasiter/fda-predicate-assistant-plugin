#!/usr/bin/env python3
"""
Tests for Combination Product Detector

Validates detection of drug-device, device-biologic, and drug-device-biologic
combination products per 21 CFR Part 3.

Author: FDA Tools Plugin Development Team
Date: 2026-02-14
"""

import sys
import os
import pytest

# Add lib directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lib'))

from combination_detector import CombinationProductDetector, detect_combination_product


class TestDrugDeviceDetection:
    """Test detection of drug-device combination products."""

    def test_drug_eluting_stent_high_confidence(self):
        """Drug-eluting stent with specific drug name should be HIGH confidence."""
        device_data = {
            'device_description': 'A coronary stent system with a drug-eluting coating containing paclitaxel',
            'trade_name': 'CardioStent DES',
            'intended_use': 'Treatment of coronary artery disease'
        }
        detector = CombinationProductDetector(device_data)
        result = detector.detect()

        assert result['is_combination'] == True
        assert result['combination_type'] == 'drug-device'
        assert result['confidence'] == 'HIGH'
        assert 'paclitaxel' in result['detected_components']
        assert result['rho_assignment'] == 'CDRH'
        assert result['consultation_required'] == 'CDER'

    def test_drug_coated_balloon_medium_confidence(self):
        """Drug-coated balloon without specific drug name should be MEDIUM confidence."""
        device_data = {
            'device_description': 'A drug-coated angioplasty balloon for peripheral intervention',
            'trade_name': 'VascuBalloon DCB',
            'intended_use': 'Dilation of peripheral arteries'
        }
        detector = CombinationProductDetector(device_data)
        result = detector.detect()

        assert result['is_combination'] == True
        assert result['combination_type'] == 'drug-device'
        assert result['confidence'] in ['MEDIUM', 'HIGH']  # Either is acceptable
        assert 'drug-coated' in result['detected_components']
        assert result['rho_assignment'] == 'CDRH'

    def test_antibiotic_bone_cement(self):
        """Antibiotic-loaded bone cement should be detected as drug-device."""
        device_data = {
            'device_description': 'PMMA bone cement with gentamicin antibiotic for infection prevention',
            'trade_name': 'OrthoCement-G',
            'intended_use': 'Fixation of orthopedic prostheses with antimicrobial protection'
        }
        detector = CombinationProductDetector(device_data)
        result = detector.detect()

        assert result['is_combination'] == True
        assert result['combination_type'] == 'drug-device'
        assert result['confidence'] == 'HIGH'
        assert 'gentamicin' in result['detected_components']

    def test_drug_free_device_exclusion(self):
        """Device explicitly marked as drug-free should NOT be detected as combination."""
        device_data = {
            'device_description': 'A drug-free bare metal stent for coronary intervention',
            'trade_name': 'BasicStent',
            'intended_use': 'Treatment of coronary artery stenosis'
        }
        detector = CombinationProductDetector(device_data)
        result = detector.detect()

        assert result['is_combination'] == False
        assert result['combination_type'] is None
        assert result['rho_assignment'] == 'CDRH'


class TestDeviceBiologicDetection:
    """Test detection of device-biologic combination products."""

    def test_collagen_matrix(self):
        """Collagen-based device should be detected as device-biologic."""
        device_data = {
            'device_description': 'Acellular collagen matrix for soft tissue reconstruction',
            'trade_name': 'DermMatrix',
            'intended_use': 'Wound coverage and soft tissue reinforcement'
        }
        detector = CombinationProductDetector(device_data)
        result = detector.detect()

        assert result['is_combination'] == True
        assert result['combination_type'] == 'device-biologic'
        assert result['confidence'] in ['MEDIUM', 'HIGH']
        assert 'collagen' in result['detected_components']
        assert result['rho_assignment'] == 'CDRH'
        assert result['consultation_required'] == 'CBER'

    def test_cell_based_product(self):
        """Cell-seeded device should be detected with UNCERTAIN RHO."""
        device_data = {
            'device_description': 'Cell-seeded tissue-engineered scaffold with autologous cells for cartilage repair',
            'trade_name': 'CartiGrow Cell Therapy',
            'intended_use': 'Cartilage defect regeneration'
        }
        detector = CombinationProductDetector(device_data)
        result = detector.detect()

        assert result['is_combination'] == True
        assert result['combination_type'] == 'device-biologic'
        assert result['confidence'] == 'HIGH'
        assert any('cell' in comp for comp in result['detected_components'])
        assert 'UNCERTAIN' in result['rho_assignment'] or result['rho_assignment'] == 'CBER'

    def test_xenograft_tissue(self):
        """Xenograft tissue device should be detected as device-biologic."""
        device_data = {
            'device_description': 'Porcine xenograft heart valve, decellularized',
            'trade_name': 'BioValve Porcine',
            'intended_use': 'Replacement of diseased heart valve'
        }
        detector = CombinationProductDetector(device_data)
        result = detector.detect()

        assert result['is_combination'] == True
        assert result['combination_type'] == 'device-biologic'
        assert 'xenograft' in result['detected_components']


class TestDrugDeviceBiologicDetection:
    """Test detection of complex drug-device-biologic products."""

    def test_drug_eluting_tissue_scaffold(self):
        """Device with both drug and biologic components should be detected."""
        device_data = {
            'device_description': 'Collagen scaffold with drug-eluting coating containing growth factor BMP-2',
            'trade_name': 'OsteoGen Plus',
            'intended_use': 'Bone regeneration with bioactive enhancement'
        }
        detector = CombinationProductDetector(device_data)
        result = detector.detect()

        assert result['is_combination'] == True
        assert result['combination_type'] == 'drug-device-biologic'
        assert result['rho_assignment'] == 'UNCERTAIN'
        assert result['consultation_required'] == 'CDER and CBER'
        # Should recommend OCP RFD
        assert any('OCP' in rec and 'RFD' in rec for rec in result['recommendations'])


class TestStandardDevices:
    """Test that standard devices are not falsely detected as combination products."""

    def test_mechanical_stent(self):
        """Standard bare metal stent should not be combination product."""
        device_data = {
            'device_description': 'Cobalt-chromium coronary stent for vessel support',
            'trade_name': 'MetalStent Pro',
            'intended_use': 'Treatment of coronary artery stenosis'
        }
        detector = CombinationProductDetector(device_data)
        result = detector.detect()

        assert result['is_combination'] == False
        assert result['combination_type'] is None
        assert result['rho_assignment'] == 'CDRH'

    def test_surgical_instrument(self):
        """Surgical instrument should not be combination product."""
        device_data = {
            'device_description': 'Stainless steel surgical scalpel with disposable blade',
            'trade_name': 'SurgiCut Elite',
            'intended_use': 'General surgical cutting'
        }
        detector = CombinationProductDetector(device_data)
        result = detector.detect()

        assert result['is_combination'] == False

    def test_compatible_with_drug_not_combination(self):
        """Device compatible with drugs but not a combination product."""
        device_data = {
            'device_description': 'Infusion pump compatible with various medications',
            'trade_name': 'InfusPro 3000',
            'intended_use': 'Administration of fluids and medications'
        }
        detector = CombinationProductDetector(device_data)
        result = detector.detect()

        # Should not detect as combination because of "compatible with" exclusion
        assert result['is_combination'] == False


class TestConvenienceFunction:
    """Test the convenience wrapper function."""

    def test_convenience_function(self):
        """Test detect_combination_product convenience function."""
        result = detect_combination_product(
            device_description='Drug-eluting stent with sirolimus coating',
            trade_name='CardioStent Plus',
            intended_use='Treatment of coronary artery disease'
        )

        assert result['is_combination'] == True
        assert result['combination_type'] == 'drug-device'
        assert 'sirolimus' in result['detected_components']


class TestRecommendations:
    """Test regulatory recommendations generation."""

    def test_drug_device_recommendations(self):
        """Drug-device should have drug-specific recommendations."""
        device_data = {
            'device_description': 'Drug-eluting stent with paclitaxel',
            'trade_name': 'Test',
            'intended_use': 'Coronary intervention'
        }
        detector = CombinationProductDetector(device_data)
        result = detector.detect()

        recommendations = result['recommendations']
        assert any('PMOA' in rec for rec in recommendations)
        assert any('drug component specifications' in rec for rec in recommendations)
        assert any('ISO 10993' in rec for rec in recommendations)

    def test_device_biologic_recommendations(self):
        """Device-biologic should have biologic-specific recommendations."""
        device_data = {
            'device_description': 'Collagen matrix for wound healing',
            'trade_name': 'Test',
            'intended_use': 'Soft tissue repair'
        }
        detector = CombinationProductDetector(device_data)
        result = detector.detect()

        recommendations = result['recommendations']
        assert any('biologic component specifications' in rec for rec in recommendations)
        assert any('immunogenicity' in rec for rec in recommendations)
        assert any('disease transmission' in rec for rec in recommendations)

    def test_complex_combination_ocp_rfd_recommendation(self):
        """Complex combinations should strongly recommend OCP RFD."""
        device_data = {
            'device_description': 'Cell-seeded scaffold with drug-eluting coating',
            'trade_name': 'Test',
            'intended_use': 'Tissue regeneration'
        }
        detector = CombinationProductDetector(device_data)
        result = detector.detect()

        recommendations = result['recommendations']
        # Should have STRONG recommendation for OCP RFD
        ocp_recs = [rec for rec in recommendations if 'OCP' in rec and 'RFD' in rec]
        assert len(ocp_recs) > 0
        assert any('STRONGLY RECOMMEND' in rec for rec in ocp_recs)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
