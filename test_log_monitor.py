#!/usr/bin/env python3
"""
Simple tests for log monitor
"""

import unittest
import tempfile
import os
from log_monitor import process_logs, parse_time

class TestLogMonitor(unittest.TestCase):
    
    def test_parse_time(self):
        """Test time parsing"""
        time_obj = parse_time("11:35:23")
        self.assertEqual(time_obj.hour, 11)
        self.assertEqual(time_obj.minute, 35)
        self.assertEqual(time_obj.second, 23)
    
    def test_process_logs(self):
        """Test log processing with sample data"""
        # Create temporary test file
        test_data = """11:35:23,test job 1, START,1001
11:35:56,test job 1, END,1001
11:36:11,test job 2, START,1002
11:42:11,test job 2, END,1002"""
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
            f.write(test_data)
            temp_filename = f.name
        
        try:
            jobs = process_logs(temp_filename)
            
            # Should have 2 completed jobs
            self.assertEqual(len(jobs), 2)
            
            # Check first job (33 seconds = 0.55 minutes)
            job1 = next(j for j in jobs if j['pid'] == 1001)
            self.assertAlmostEqual(job1['duration_minutes'], 0.55, places=1)
            
            # Check second job (6 minutes)
            job2 = next(j for j in jobs if j['pid'] == 1002)
            self.assertAlmostEqual(job2['duration_minutes'], 6.0, places=1)
            
        finally:
            os.unlink(temp_filename)

if __name__ == '__main__':
    unittest.main()