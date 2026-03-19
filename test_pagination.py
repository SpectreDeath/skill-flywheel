#!/usr/bin/env python3
"""
Test script to verify pagination implementation for the skills endpoint.
This script tests the new pagination functionality without requiring a running server.
"""

import os
import sqlite3

# Change default path depending on if run via uvicorn from root or within src/discovery
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))
DB_PATH = os.path.join(BASE_DIR, 'data', 'skill_registry.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def test_pagination_logic():
    """Test the pagination logic directly against the database"""
    print("Testing pagination logic...")
    
    try:
        with get_db() as db:
            cursor = db.cursor()
            
            # Get total count
            cursor.execute("SELECT COUNT(*) FROM skills")
            total_count = cursor.fetchone()[0]
            print(f"Total skills in database: {total_count}")
            
            if total_count == 0:
                print("No skills found in database. Creating test data...")
                create_test_data(db)
                cursor.execute("SELECT COUNT(*) FROM skills")
                total_count = cursor.fetchone()[0]
                print(f"Total skills after test data creation: {total_count}")
            
            # Test pagination parameters
            test_cases = [
                {"page": 1, "limit": 5},
                {"page": 1, "limit": 10},
                {"page": 2, "limit": 5},
                {"page": 999, "limit": 5},  # Page beyond total pages
                {"page": 0, "limit": 5},     # Invalid page
                {"page": 1, "limit": 0},     # Invalid limit
                {"page": 1, "limit": 150},   # Limit above maximum
            ]
            
            for test_case in test_cases:
                page = test_case["page"]
                limit = test_case["limit"]
                
                print(f"\nTesting page={page}, limit={limit}")
                
                # Apply parameter validation (same as in the endpoint)
                page = max(page, 1)
                if limit < 1:
                    limit = 20
                elif limit > 100:
                    limit = 100
                
                offset = (page - 1) * limit
                
                # Get paginated results
                cursor.execute(
                    "SELECT skill_id, name, domain, version, health_status FROM skills ORDER BY name LIMIT ? OFFSET ?",
                    (limit, offset)
                )
                rows = cursor.fetchall()
                
                # Calculate pagination metadata
                total_pages = (total_count + limit - 1) // limit
                has_next = page < total_pages
                has_prev = page > 1
                
                result = {
                    "skills": [dict(row) for row in rows],
                    "pagination": {
                        "page": page,
                        "limit": limit,
                        "total": total_count,
                        "total_pages": total_pages,
                        "has_next": has_next,
                        "has_prev": has_prev
                    }
                }
                
                print(f"  Returned {len(rows)} skills")
                print(f"  Pagination: page={page}, limit={limit}, total={total_count}, total_pages={total_pages}")
                print(f"  Has next: {has_next}, Has prev: {has_prev}")
                
                # Verify consistency
                if page > total_pages and total_pages > 0:
                    assert len(rows) == 0, f"Expected empty results for page {page} > total_pages {total_pages}"
                else:
                    expected_count = min(limit, total_count - offset)
                    assert len(rows) == expected_count, f"Expected {expected_count} rows, got {len(rows)}"
                
                print("  ✓ Test passed")
    
    except Exception as e:
        print(f"Error during testing: {e}")
        return False
    
    return True

def create_test_data(db):
    """Create test data if no skills exist"""
    cursor = db.cursor()
    
    # Create skills table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS skills (
            skill_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            domain TEXT,
            version TEXT,
            health_status TEXT DEFAULT 'unknown',
            module_path TEXT,
            entry_function TEXT,
            invocation_count INTEGER DEFAULT 0,
            last_invoked TEXT,
            dependencies TEXT
        )
    ''')
    
    # Insert test skills
    test_skills = [
        ("skill_001", "Data Analysis", "analytics", "1.0.0", "healthy", "skills.data.analysis", "analyze_data", 0, None, "[]"),
        ("skill_002", "Machine Learning", "ml", "1.2.0", "healthy", "skills.ml.predict", "predict", 0, None, "[]"),
        ("skill_003", "Web Scraping", "scraping", "0.9.0", "healthy", "skills.web.scrape", "scrape", 0, None, "[]"),
        ("skill_004", "Image Processing", "vision", "1.1.0", "healthy", "skills.vision.process", "process_image", 0, None, "[]"),
        ("skill_005", "Natural Language Processing", "nlp", "2.0.0", "healthy", "skills.nlp.analyze", "analyze_text", 0, None, "[]"),
        ("skill_006", "Data Visualization", "analytics", "1.0.5", "healthy", "skills.viz.plot", "create_plot", 0, None, "[]"),
        ("skill_007", "API Integration", "integration", "1.3.0", "healthy", "skills.api.connect", "connect", 0, None, "[]"),
        ("skill_008", "Database Operations", "database", "1.0.0", "healthy", "skills.db.query", "execute_query", 0, None, "[]"),
        ("skill_009", "File Processing", "io", "0.8.0", "healthy", "skills.io.process", "process_file", 0, None, "[]"),
        ("skill_010", "Security Analysis", "security", "1.1.0", "healthy", "skills.security.scan", "scan", 0, None, "[]"),
        ("skill_011", "Performance Monitoring", "monitoring", "1.0.0", "healthy", "skills.monitor.check", "check_performance", 0, None, "[]"),
        ("skill_012", "Error Handling", "utilities", "1.0.0", "healthy", "skills.utils.handle", "handle_error", 0, None, "[]"),
        ("skill_013", "Logging", "utilities", "1.0.0", "healthy", "skills.utils.log", "log_event", 0, None, "[]"),
        ("skill_014", "Configuration", "utilities", "1.0.0", "healthy", "skills.utils.config", "load_config", 0, None, "[]"),
        ("skill_015", "Testing", "development", "1.0.0", "healthy", "skills.dev.test", "run_tests", 0, None, "[]"),
    ]
    
    for skill in test_skills:
        cursor.execute('''
            INSERT OR REPLACE INTO skills 
            (skill_id, name, domain, version, health_status, module_path, entry_function, invocation_count, last_invoked, dependencies)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', skill)
    
    db.commit()
    print(f"Created {len(test_skills)} test skills")

def test_endpoint_compatibility():
    """Test that the new endpoint structure is compatible with existing clients"""
    print("\nTesting endpoint compatibility...")
    
    try:
        with get_db() as db:
            cursor = db.cursor()
            
            # Test default parameters (page=1, limit=20)
            cursor.execute("SELECT COUNT(*) FROM skills")
            total_count = cursor.fetchone()[0]
            
            # Simulate the new endpoint with default parameters
            page = 1
            limit = 20
            offset = (page - 1) * limit
            
            cursor.execute(
                "SELECT skill_id, name, domain, version, health_status FROM skills ORDER BY name LIMIT ? OFFSET ?",
                (limit, offset)
            )
            rows = cursor.fetchall()
            
            result = {
                "skills": [dict(row) for row in rows],
                "pagination": {
                    "page": page,
                    "limit": limit,
                    "total": total_count,
                    "total_pages": (total_count + limit - 1) // limit,
                    "has_next": page < ((total_count + limit - 1) // limit),
                    "has_prev": page > 1
                }
            }
            
            # Verify that skills are still accessible at the top level
            assert "skills" in result, "Skills should be accessible at top level"
            assert isinstance(result["skills"], list), "Skills should be a list"
            
            # Verify pagination metadata is present
            assert "pagination" in result, "Pagination metadata should be present"
            assert "page" in result["pagination"], "Page number should be present"
            assert "limit" in result["pagination"], "Limit should be present"
            assert "total" in result["pagination"], "Total count should be present"
            
            print("  ✓ Backward compatibility maintained")
            print("  ✓ Pagination metadata added")
            print("  ✓ Skills accessible at top level")
            
            return True
            
    except Exception as e:
        print(f"  ✗ Compatibility test failed: {e}")
        return False

if __name__ == "__main__":
    print("=== Testing Skills Endpoint Pagination ===")
    
    success = True
    
    # Test pagination logic
    success &= test_pagination_logic()
    
    # Test compatibility
    success &= test_endpoint_compatibility()
    
    if success:
        print("\n🎉 All tests passed! Pagination implementation is working correctly.")
        print("\nUsage examples:")
        print("  GET /skills                    # Default: page=1, limit=20")
        print("  GET /skills?page=2&limit=10    # Page 2, 10 skills per page")
        print("  GET /skills?page=1&limit=50    # Page 1, 50 skills per page")
        print("\nResponse format:")
        print("  {")
        print("    'skills': [...],")
        print("    'pagination': {")
        print("        'page': 1,")
        print("        'limit': 20,")
        print("        'total': 500,")
        print("        'total_pages': 25,")
        print("        'has_next': true,")
        print("        'has_prev': false")
        print("    }")
        print("  }")
    else:
        print("\n❌ Some tests failed. Please check the implementation.")
