import pygame
import numpy as np

"""
TODO:
- Need to add documentation/comments
- Test implementation edit: working
- Optimise by using numpy arrays instead especially removing the loop to add items from children trees in contained_by method
- Expand to include rectangles
"""

class Point():
    """
    Simple class that is being used as a "struct" to hold coordinate data
    """
    def __init__(self, x, y, object=None):
        self.x = x
        self.y = y
        self.object = object

class AABB():
    """
    Class representing an AABB.
    """
    def __init__(self, centre :Point, half_width, half_height):
        self._centre = centre
        self._half_width = half_width
        self._half_height = half_height

        self._top_left = Point(self._centre.x - self._half_width, self._centre.y - self._half_height)
        self._top_right = Point(self._centre.x + self._half_width, self._centre.y - self._half_height)
        self._bottom_left = Point(self._centre.x - self._half_width, self._centre.y + self._half_height)
        self._bottom_right = Point(self._centre.x - self._half_width, self._centre.y + self._half_height)
    
    def get_centre(self):
        return self._centre
    
    def get_half_width(self):
        return self._half_width
    
    def get_half_height(self):
        return self._half_height

    def get_top_left(self):
        return self._top_left

    def get_top_right(self):
        return self._top_right

    def get_bottom_left(self):
        return self._bottom_left

    def get_bottom_right(self):
        return self._bottom_right

    def contains_point(self, point :pygame.Vector2):
        return not (point.x > self._top_right.x 
                    or point.x < self._top_left.x 
                    or point.y > self._bottom_right.y 
                    or point.y < self._top_left.y)
    
    def intersects(self, other):
        if type(other) is AABB:
            return not (other.get_top_left().x > self._top_right.x 
                    or other.get_top_right().x < self._top_left.x 
                    or other.get_top_left().y > self._bottom_right.y 
                    or other.get_bottom_right().y < self._top_left.y)
    
    def draw(self, screen):
        pygame.draw.rect(screen, (255,255,255), [self._top_left.x, self._top_left.y, self._half_width*2, self._half_height*2], 1)

class QuadTree():
    def __init__(self, centre, half_width, half_height, level):
        self._capacity = 4
        self._level = level

        self._boundry = AABB(centre, half_width, half_height)

        self._items = []

        self._north_west = None
        self._north_east = None
        self._south_west = None
        self._south_east = None

    def insert(self, item):
        # if the item is not within this trees area
        if not self._boundry.contains_point(item.get_position()):
            return False
        
        if (len(self._items) < self._capacity and self._north_west == None):
            self._items.append(item)
            return True
        
        if (self._north_west == None):
            if not (self.subdivide()):
                return False
        
        if (self._north_west.insert(item)):
            return True
        if (self._north_east.insert(item)):
            return True
        if (self._south_west.insert(item)):
            return True
        if (self._south_east.insert(item)):
            return True
        
        print("problem inserting " + str((item.get_position().x, item.get_position().y)) + " in level: " + str(self._level))
        return False

    def subdivide(self):
        new_half_width = self._boundry.get_half_width() / 2
        new_half_height = self._boundry.get_half_height() / 2

        centre = self._boundry.get_centre()
        north_west_centre = Point(centre.x - new_half_width, centre.y - new_half_height)
        north_east_centre = Point(centre.x + new_half_width, centre.y - new_half_height)
        south_west_centre = Point(centre.x - new_half_width, centre.y + new_half_height)
        south_east_centre = Point(centre.x + new_half_width, centre.y + new_half_height)

        self._north_west = QuadTree(north_west_centre, new_half_width, new_half_height, self._level + 1)
        self._north_east = QuadTree(north_east_centre, new_half_width, new_half_height, self._level + 1)
        self._south_west = QuadTree(south_west_centre, new_half_width, new_half_height, self._level + 1)
        self._south_east = QuadTree(south_east_centre, new_half_width, new_half_height, self._level + 1)

        for i in reversed(self._items):
            if (self._north_west.insert(i)):
                del self._items[-1]
                continue
            if (self._north_east.insert(i)):
                del self._items[-1]
                continue
            if (self._south_west.insert(i)):
                del self._items[-1]
                continue
            if (self._south_east.insert(i)):
                del self._items[-1]
                continue
            print("problem subdividing")
            return False
        return True
        
    def contained_by(self, search_area):
        items_in_range = []
        
        if not (self._boundry.intersects(search_area)):
            return items_in_range
        
        for item in self._items:
            if search_area.contains_point(item.get_position()):
                items_in_range.append(item)
            
        if self._north_west == None:
            return items_in_range
        
        for i in self._north_west.contained_by(search_area):
            items_in_range.append(i)
        for i in self._north_east.contained_by(search_area):
            items_in_range.append(i)
        for i in self._south_west.contained_by(search_area):
            items_in_range.append(i)
        for i in self._south_east.contained_by(search_area):
            items_in_range.append(i)
        
        return items_in_range
    
    def draw_tree(self, screen):
        if not self._north_west == None:
            self._north_west.draw_tree(screen)
            self._north_east.draw_tree(screen)
            self._south_west.draw_tree(screen)
            self._south_east.draw_tree(screen)

        self._boundry.draw(screen)
    
    def display(self):
        print("Level: " + str(self._level) + " No. Items: "+ str(len(self._items)))
        if not self._north_west == None:
            self._north_west.display()
            self._north_east.display()
            self._south_west.display()
            self._south_east.display()

    def clear_tree(self):
        self._items = []
        self._north_west = None
        self._north_east = None
        self._south_west = None
        self._south_east = None

def main():
    centre1 = Point(100,100)
    rect1 = AABB(centre1, 50, 50)

    centre2 = Point(150,50)
    rect2 = AABB(centre2, 50, 50)

    print(rect1.contains_point(centre2))

if __name__ == "__main__":
    main()